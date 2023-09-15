import requests
from requests.exceptions import HTTPError
from configparser import ConfigParser
import argparse
import urllib3
import sys
from pprint import pp

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
    
def make_api_req(query_params):
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



if __name__ == "__main__":
    user_args = read_user_cli_args()
    #make_api_req_to_weather(user_args.city, user_args.imperial)
    
    q_params = build_weather_query(user_args.city, user_args.imperial)
    d = make_api_req(q_params)
    temp = "F" if user_args.imperial else "C"
    print(f"{d['name']}: "
          f"{d['weather'][0]['description']}"
          f" ({d['main']['temp']} {temp})"
          )