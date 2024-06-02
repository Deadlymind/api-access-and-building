from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup as bs
import logging
from cachetools import TTLCache

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a cache with a TTL (time-to-live) of 10 minutes and a max size of 100 entries
cache = TTLCache(maxsize=100, ttl=600)

def get_currency(in_currency, out_currency):
    """
    Fetch the exchange rate from x-rates.com for the given input and output currencies.

    Parameters:
    in_currency (str): The currency code to convert from.
    out_currency (str): The currency code to convert to.

    Returns:
    float: The exchange rate.
    """
    url = f"https://www.x-rates.com/calculator/?from={in_currency}&to={out_currency}&amount=1"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = bs(response.text, "html.parser")
        rate = soup.find("span", class_="ccOutputRslt").get_text()
        rate = float(rate[:-4])  # Remove the last 4 characters (usually ' USD' or similar)
        logging.info(f"Fetched rate for {in_currency} to {out_currency}: {rate}")
        return rate
    except (requests.RequestException, AttributeError, ValueError) as e:
        logging.error(f"Error fetching currency rate: {e}")
        return None  # You may want to raise an exception or return a default value

app = Flask(__name__)

@app.route("/")
def home():
    """
    Home route to provide basic information about the API.
    """
    return "<h1>Currency Rate REST API</h1><p>Example URL: /api/v1/usd-eur</p>"

@app.route("/api/v1/<string:in_cur>-<string:out_cur>")
def api(in_cur, out_cur):
    """
    API route to get the exchange rate between two currencies.

    Parameters:
    in_cur (str): The input currency code.
    out_cur (str): The output currency code.

    Returns:
    Response: JSON response containing the input currency, output currency, and exchange rate.
    """
    # Check if the rate is cached
    cache_key = f"{in_cur}-{out_cur}"
    if cache_key in cache:
        rate = cache[cache_key]
        logging.info(f"Rate for {in_cur} to {out_cur} fetched from cache: {rate}")
    else:
        rate = get_currency(in_cur, out_cur)
        if rate is not None:
            cache[cache_key] = rate  # Cache the rate
        else:
            return jsonify({"error": "Unable to fetch currency rate"}), 500

    result_dict = {'input_currency': in_cur, 'output_currency': out_cur, 'rate': rate}
    return jsonify(result_dict)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Specify the port explicitly for clarity
