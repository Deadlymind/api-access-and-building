import requests  # Import the requests library to make HTTP requests
import json  # Import the JSON library to parse JSON responses
import logging  # Import the logging library for error handling

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(url):
    """
    Fetch data from the given URL.

    Parameters:
    url (str): The URL to fetch data from.

    Returns:
    dict: The parsed JSON data if the request is successful.
    None: If the request fails.
    """
    try:
        response = requests.get(url)  # Make the GET request to the URL
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()  # Parse the JSON content of the response
        logging.info("Data fetched successfully")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding failed: {e}")
        return None

def main():
    # Replace 'url here + apikey' with your actual URL and API key
    url = 'url here + apikey'

    data = fetch_data(url)  # Fetch the data from the URL

    if data:
        print(type(data))  # Print the type of the data
        # Ensure the expected keys are in the data to avoid KeyError
        if 'images' in data and '0' in data['images']:
            print(data['images']['0'])  # Print the first image data
        else:
            logging.error("Expected keys 'images' and '0' not found in the data")
    else:
        logging.error("No data to display")

if __name__ == "__main__":
    main()
