import os
from threading import Lock
from typing import Optional, Tuple

import gradio as gr
from dotenv import load_dotenv

from query_data import get_custom_prompt_qa_chain

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(OPENAI_API_KEY)


def set_openai_api_key():
    """Set the api key and return chain."""
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    chain = get_custom_prompt_qa_chain()
    os.environ["OPENAI_API_KEY"] = ""
    return chain


class ChatWrapper:
    def __init__(self):
        self.lock = Lock()

    def __call__(self, inp: str, history: Optional[Tuple[str, str]], chain):
        """Execute the chat functionality."""
        self.lock.acquire()
        try:
            history = history or []
            # If chain is None, that is because no API key was provided.
            if chain is None:
                history.append((inp, "Please paste your OpenAI key to use"))
                return history, history
            # Set OpenAI key
            import openai

            openai.api_key = OPENAI_API_KEY
            # Run chain and append input.
            output = chain({"question": inp})["answer"]
            history.append((inp, output))
        except Exception as e:
            raise e
        finally:
            self.lock.release()
        return history, history


chat = ChatWrapper()

block = gr.Blocks(css="#component-0 {padding: 4rem}", theme=gr.themes.Soft())

with block:
    with gr.Row():
        gr.Markdown("<h1><center>Lean Manufacturing Chatbot</center></h1>")

    chatbot = gr.Chatbot()

    with gr.Row():
        message = gr.Textbox(
            label="What's your question?",
            placeholder="Ask questions about Lean Manufacturing",
            lines=1,
            scale=2,
        )
        submit = gr.Button(value="Send", variant="primary", scale=1)

    gr.Examples(
        examples=[
            "What is Lean Manufacturing?",
            "what is the difference between lean and six sigma?",
            "what is OEE (Overall Equipment Effectiveness) and how to calculate it?",
        ],
        inputs=message,
    )

    state = gr.State()
    agent_state = gr.State()

    submit.click(
        chat,
        inputs=[message, state, agent_state],
        outputs=[chatbot, state],
    )
    message.submit(
        chat,
        inputs=[message, state, agent_state],
        outputs=[chatbot, state],
    )

    message.change(
        set_openai_api_key,
        inputs=[],
        outputs=[agent_state],
    )

block.launch(debug=True, share=True)
