import requests  # Import the requests library to make HTTP requests
import json  # Import the JSON library for saving articles to a file
import csv  # Import the CSV library for saving articles to a CSV file
import logging  # Import the logging library for error handling

# Setup logging
logging.basicConfig(filename='news_api.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_news(country, api_key='d6977929ea8441638de5dfbfd214df3d', save_to_file=None, file_format='json', page_size=100):
    """
    Fetch and print top news headlines based on a country.

    Parameters:
    country (str): The country to fetch top headlines for.
    api_key (str): Your News API key.
    save_to_file (str): The file name to save the articles (default is None).
    file_format (str): The format to save the file ('json' or 'csv', default is 'json').
    page_size (int): The number of articles to fetch per page (default is 100).

    Returns:
    None
    """
    url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}&pageSize={page_size}'
    articles = []
    page = 1
    total_results = None

    try:
        while True:
            response = requests.get(f"{url}&page={page}")
            response.raise_for_status()  # Raise an HTTPError for bad responses
            content = response.json()

            # Check if the API response status is 'ok'
            if content.get('status') == 'ok':
                if total_results is None:
                    total_results = content.get('totalResults', 0)

                articles.extend(content.get('articles', []))
                if len(articles) >= total_results:
                    break
                page += 1
            else:
                logging.error("Failed to fetch articles: %s", content.get('message'))
                print("Failed to fetch articles:", content.get('message'))
                return

        for article in articles:  # Iterate through each article in the list
            # Print the title and description of each article
            print(f"TITLE: {article['title']} \nDESCRIPTION: {article['description']}")

        # Save articles to a file if specified
        if save_to_file:
            if file_format == 'json':
                with open(save_to_file, 'w') as json_file:
                    json.dump(articles, json_file, indent=4)
                print(f"Articles saved to {save_to_file}")
            elif file_format == 'csv':
                with open(save_to_file, 'w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=articles[0].keys())
                    writer.writeheader()
                    writer.writerows(articles)
                print(f"Articles saved to {save_to_file}")
            else:
                print("Unsupported file format. Please use 'json' or 'csv'.")
    except requests.exceptions.RequestException as e:
        logging.error("Request failed: %s", e)
        print("Request failed:", e)

# Example usage of the get_news function with additional features
get_news('us', save_to_file='top_headlines.json', file_format='json')
