import requests
import random


#api setup
#---------------------------------------------------------------
def get_data_as_json(endpoint, headers):
    response = requests.get(endpoint, headers = headers)#raise error if api failed
    if response:
        print("API accessed successfully.")
    else:
        raise Exception(f"Non-success status code: {response.status_code}")
    return response.json()

user_agent = "jaysonc678@gmail.com"

#needed to access api
BASE_URL = "https://api.weather.gov"
headers = {'User-Agent' : f'{user_agent}'}

def coords_to_gridpoints(coordinates):
    coordinate_endpoint = f"{BASE_URL}/points/{coordinates[0]},{coordinates[1]}"

    coordinate_data = get_data_as_json(coordinate_endpoint, headers)["properties"]
    station_and_coords = [coordinate_data["gridId"], coordinate_data["gridX"], coordinate_data["gridY"]]
    return station_and_coords

def forecast_from_gridpoints(station_and_coords):
    forecast_endpoint = f"{BASE_URL}/gridpoints/{station_and_coords[0]}/{station_and_coords[1]},{station_and_coords[2]}/forecast"
    #get info from api then get specifically the first period
    forecast_data = get_data_as_json(forecast_endpoint, headers)["properties"]["periods"][0]

    #save the forecast in lowercase
    weather = forecast_data["shortForecast"].lower()
    return weather

def get_weather(coords = [32.9004,-105.9629]):
    return forecast_from_gridpoints(coords_to_gridpoints(coords))