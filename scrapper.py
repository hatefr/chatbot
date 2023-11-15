import json

import wikipediaapi


def scrape_wikipedia(topic, depth=1):
    # Specify a custom user agent string
    custom_user_agent = "YourBot/1.0 (hatef.rahmani.f@email.com)"

    # Create a Wikipedia instance with the custom user agent
    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent=custom_user_agent
    )  # pylint: disable=invalid-name

    # Get the main page on the given topic
    page = wiki_wiki.page(topic)

    if not page.exists():
        print(f"Page for '{topic}' does not exist on Wikipedia.")
        return None

    print(f"Scraping information on '{topic}'...")

    # Initialize an empty dictionary to store page titles and content
    data = {}

    # Recursive function to traverse links up to the specified depth
    def traverse_links(current_page, current_depth):
        nonlocal data

        if current_depth > depth:
            return

        # Add the current page's title and content to the data dictionary
        data[current_page.title] = current_page.text

        # Recursively traverse links on the current page
        for link in current_page.links.values():
            traverse_links(link, current_depth + 1)

    # Start traversing links from the main page
    traverse_links(page, 0)

    return data


if __name__ == "__main__":
    topic_to_scrape = "Lean manufacturing"

    # Set the depth for link traversal
    traversal_depth = 1

    # Scrape Wikipedia for information
    result_data = scrape_wikipedia(topic_to_scrape, depth=traversal_depth)

    # Save the scraped data to a json file
    # if result_data:
    #     with open(
    #         f"knowledge/{topic_to_scrape}_wikipedia_data.json", "w", encoding="utf-8"
    #     ) as json_file:
    #         json.dump(result_data, json_file, indent=4)

    #     print(f"Scraped data saved to {topic_to_scrape}_wikipedia_data.json.")
    # else:
    #     print("No data scraped.")

    # Save the scraped data to a txt file
    if result_data:
        with open(
            f"knowledge_base/{topic_to_scrape}_wikipedia_data.txt",
            "w",
            encoding="utf-8",
        ) as txt_file:
            for title, content in result_data.items():
                txt_file.write(f"{title}\n\n{content}\n\n")

        print(f"Scraped data saved to {topic_to_scrape}_wikipedia_data.txt.")
    else:
        print("No data scraped.")
