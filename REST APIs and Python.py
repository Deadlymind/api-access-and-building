import requests  # Import the requests library to make HTTP requests
import json  # Import the JSON library for saving articles to a file
import csv  # Import the CSV library for saving articles to a CSV file
import logging  # Import the logging library for error handling

# Setup logging
logging.basicConfig(filename='news_api.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_news(topic, from_date, to_date, api_key='d6977929ea8441638de5dfbfd214df3d', language='en', save_to_file=None, file_format='json'):
    """
    Fetch and print news articles based on a topic within a specified date range.

    Parameters:
    topic (str): The topic to search for in the news articles' titles.
    from_date (str): The start date for fetching news articles (YYYY-MM-DD).
    to_date (str): The end date for fetching news articles (YYYY-MM-DD).
    api_key (str): Your News API key.
    language (str): The language of the news articles (default is 'en' for English).
    save_to_file (str): The file name to save the articles (default is None).
    file_format (str): The format to save the file ('json' or 'csv', default is 'json').

    Returns:
    None
    """
    # Construct the URL for the API request with the specified parameters
    url = f'https://newsapi.org/v2/everything?qInTitle={topic}&from={from_date}&to={to_date}&sortBy=popularity&language={language}&apiKey={api_key}'

    try:
        response = requests.get(url)  # Make the GET request to the News API
        response.raise_for_status()  # Raise an HTTPError for bad responses
        content = response.json()  # Parse the JSON content of the response

        # Check if the API response status is 'ok'
        if content.get('status') == 'ok':
            articles = content.get('articles', [])  # Get the list of articles from the response
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
        else:
            logging.error("Failed to fetch articles: %s", content.get('message'))
            print("Failed to fetch articles:", content.get('message'))
    except requests.exceptions.RequestException as e:
        logging.error("Request failed: %s", e)
        print("Request failed:", e)

# Example usage of the get_news function with additional features
get_news('stock market', '2024-05-01', '2024-05-02', save_to_file='articles.json', file_format='json')
