import requests
import csv
import os
import argparse
import logging
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        filename='weather_app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'
    )

def validate_inputs(city, units):
    if not city:
        raise ValueError("City name cannot be empty.")
    if units not in ["metric", "imperial", "standard"]:
        raise ValueError("Units must be 'metric', 'imperial', or 'standard'.")

def get_weather(city="Paris", units="metric", api_key="74aae769a95b89aaf9198ad31ec95458", output_dir="."):
    validate_inputs(city, units)

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.json()

        if 'list' not in content:
            raise ValueError("Unexpected response structure from the API.")

        filename = f"weather_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(output_dir, filename)

        temperatures = []

        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Datetime", "Temperature", "Description"])

            for item in content["list"]:
                temp = item["main"]["temp"]
                temperatures.append(temp)
                writer.writerow([item["dt_txt"], temp, item["weather"][0]["description"]])

        avg_temp = sum(temperatures) / len(temperatures) if temperatures else 0

        logging.info(f"Weather data saved to {filepath}")
        logging.info(f"Average Temperature: {avg_temp:.2f} {units}")

        print(f"Weather data saved to {filepath}")
        print(f"Average Temperature: {avg_temp:.2f} {units}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        print(f"Error fetching weather data: {e}")
    except KeyError:
        logging.error("Error processing weather data. Please check the API response structure.")
        print("Error processing weather data. Please check the API response structure.")
    except ValueError as ve:
        logging.error(ve)
        print(ve)

if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser(description="Fetch weather data for a specified city.")
    parser.add_argument("--units", type=str, default="metric", choices=["metric", "imperial", "standard"], help="The unit system to use (metric, imperial, standard).")
    parser.add_argument("--output-dir", type=str, default=".", help="The directory to save the output CSV file.")
    parser.add_argument("--api-key", type=str, default="74aae769a95b89aaf9198ad31ec95458", help="Your OpenWeatherMap API key.")

    args = parser.parse_args()

    get_weather(units=args.units, api_key=args.api_key, output_dir=args.output_dir)
