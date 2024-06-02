import requests  # Import the requests library to make HTTP requests
import json  # Import the JSON library to parse JSON responses
import logging  # Import the logging library for error handling

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_text(text, language="auto"):
    """
    Check the given text for grammar and spelling errors using LanguageTool API.

    Parameters:
    text (str): The text to be checked.
    language (str): The language of the text (default is 'auto').

    Returns:
    dict: The parsed JSON response if the request is successful.
    None: If the request fails.
    """
    url = "https://api.languagetool.org/v2/check"
    data = {
        "text": text,
        "language": language
    }

    try:
        response = requests.post(url, data=data)  # Make the POST request to the LanguageTool API
        response.raise_for_status()  # Raise an HTTPError for bad responses
        result = response.json()  # Parse the JSON content of the response
        logging.info("Text checked successfully")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding failed: {e}")
        return None

def main():
    text = "tis is a nixe day!"
    language = "auto"
    
    result = check_text(text, language)  # Check the text using the LanguageTool API
    
    if result:
        print(json.dumps(result, indent=4))  # Pretty print the JSON result
    else:
        logging.error("No result to display")

if __name__ == "__main__":
    main()
