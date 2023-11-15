Chatbot-prototype

Building chatbot for your own texts using LLM from openAI API....

First, data for the desired topic was scrapped from related Wikipedia pages ('scrapper.py') for Lean Manufacturing. The text data were split into chucnkes and openAI embeddings was used to transform the text to vectors ('ingest_data.py). The vectorstore was created which then was used for prompt engineering such as RAG using LangChain library...Finally gradio was used to serve the model..... (will be updated).   
