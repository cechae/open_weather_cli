import requests
from requests.exceptions import HTTPError
from configparser import ConfigParser
import argparse
import urllib3
import sys
from pprint import pp
import pandas as pd
import matplotlib.pyplot as plt

def read_user_cli_args():
    parser = argparse.ArgumentParser(
        description = "gets weather and temperature information for a city"
    )
    parser.add_argument("city", nargs="+", type=str, help="enter the city name")
    parser.add_argument("-i", "--imperial", action="store_true", help="Display the temperature in imperial units")
    return parser.parse_args()

    
def get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]


def build_weather_query(city, imperial=False):
    """Builds the URL for an API request to OpenWeather's weather API.
    Args:
        city (List[str]): Name of a city as collected by argparse
        imperial (bool): whether or not to use imperial units. Defaults to False.
    Returns:
        str: URL formatted for a call to OpenWeather's API endpoint.
    """
    # raise an exception if the request was unsuccessful.
    API_KEY = get_api_key()
    
    query_params = {
        "q": " ".join(city),
        "appid": API_KEY,
        "units": "imperial" if imperial else "metric",
    }
    return query_params
    
def search_weather_by_city(query_params):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    try:
        r = requests.get(base_url, params = query_params)
        r.raise_for_status()
        dict = r.json() # convert the Content-Type into a Python Dictionary.
        
    except HTTPError as http_err:
        sys.exit("Can't find data for this city... Did you forget space?")
    except error as e:
        sys.exit("Other error occurred ... ")
    return dict

def search_forecast_by_city(query_params):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    try:
        r = requests.get(base_url, query_params)
        r.raise_for_status()
        dict = r.json()
    except HTTPError as http_err:
        sys.exit("Error occurred. Can't find the data for this city...")
    return dict

def visualize_data(df, cityname):
    plt.figure(figsize=(10,6))
    plt.plot(df['Date'], df['Temperature (Celsius)'], marker = 'o', linestyle='-')
    plt.xlabel("Date and Time")
    plt.ylabel("Temperature (Celsius)")
    plt.title(f"Temperature Trends in {cityname}")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig('output.png')

if __name__ == "__main__":
    user_args = read_user_cli_args()
    q_params = build_weather_query(user_args.city, user_args.imperial)
    #d = search_weather_by_city(q_params)
    r = search_forecast_by_city(q_params)
    data = []
    # extract the relevant data here.
    for item in r["list"]:
        data.append({
            "Date":item["dt_txt"],
            "Temperature (Celsius)": item["main"]["temp"]
        })
    df = pd.DataFrame(data)
    visualize_data(df, " ".join(user_args.city))
    