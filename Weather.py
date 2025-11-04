from tkinter import *
import tkinter as tk
import requests
import pgeocode



class Get_Weather:
    def __init__(self):
        super().__init__()
        #api setup
        self.user_agent = "WeatherBot"
        #needed to access api
        self.BASE_URL = "https://api.weather.gov"
        self.headers = {'User-Agent' : f'{self.user_agent}'}

    def get_data_as_json(self,endpoint, headers):
        self.response = requests.get(endpoint, headers = self.headers) #raise error if api failed
        if self.response:
            print("API accessed successfully.")
        else:
            raise Exception(f"Non-success status code: {self.response.status_code}")
        return self.response.json()


    def coords_to_gridpoints(self,coordinates):
        self.coordinate_endpoint = f"{self.BASE_URL}/points/{coordinates[0]},{coordinates[1]}"

        self.coordinate_data = self.get_data_as_json(self.coordinate_endpoint, self.headers)["properties"]
        self.location_data = self.coordinate_data["relativeLocation"]["properties"]
        self.location = f"{self.location_data["city"]}, {self.location_data["state"]}"
        self.station__coords_and_location = {"gridId":self.coordinate_data["gridId"], "x":self.coordinate_data["gridX"], "y":self.coordinate_data["gridY"], "location":self.location}
        return self.station__coords_and_location

    def forecast_from_gridpoints(self,station_and_coords):
        self.forecast_endpoint = f"{self.BASE_URL}/gridpoints/{station_and_coords["gridId"]}/{station_and_coords["x"]},{station_and_coords["y"]}/forecast"
        #get info from api then get specifically the first period
        self.forecast_data = self.get_data_as_json(self.forecast_endpoint, self.headers)["properties"]["periods"][0]

        #save the forecast in lowercase
        self.weather = self.forecast_data["shortForecast"].lower()
        self.temp = self.forecast_data["temperature"]
        return {"weather":self.weather, "temp":self.temp, "location":station_and_coords["location"]}

    def get_weather(self,zip = "88310"):
        self.nomi = pgeocode.Nominatim('us')
        self.loc_data = self.nomi.query_postal_code(zip)
        self.coords = [float(self.loc_data["latitude"]),float(self.loc_data["longitude"])]
        try:
            self.data = self.forecast_from_gridpoints(self.coords_to_gridpoints(self.coords))
        except:
            return f"Invalid zip code"
        return f"Current Weather: {self.data["weather"].title()} | Temperature: {self.data["temp"]} | Location: {self.data["location"]}"
    

