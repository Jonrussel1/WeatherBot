from tkinter import *
import tkinter as tk
import requests
import random



class Get_weather(Tk):
    

    def __init__(self):
        super().__init__()

       
       
        #api setup
        self.user_agent = "jaysonc678@gmail.com"
        #needed to access api
        self.BASE_URL = "https://api.weather.gov"
        self.headers = {'User-Agent' : f'{self.user_agent}'}

    def get_data_as_json(self,endpoint, headers):
        self.response = requests.get(endpoint, headers = headers) #raise error if api failed
        if self.response:
            print("API accessed successfully.")
        else:
            raise Exception(f"Non-success status code: {self.response.status_code}")
        return self.response.json()


    def coords_to_gridpoints(self,coordinates):
        self.coordinate_endpoint = f"{self.BASE_URL}/points/{coordinates[0]},{coordinates[1]}"

        self.coordinate_data = self.get_data_as_json(self.coordinate_endpoint, self.headers)["properties"]
        self.station_and_coords = [self.coordinate_data["gridId"], self.coordinate_data["gridX"], self.coordinate_data["gridY"]]
        return self.station_and_coords

    def forecast_from_gridpoints(self,station_and_coords):
        self.forecast_endpoint = f"{self.BASE_URL}/gridpoints/{station_and_coords[0]}/{station_and_coords[1]},{station_and_coords[2]}/forecast"
        #get info from api then get specifically the first period
        self.forecast_data = self.get_data_as_json(self.forecast_endpoint, self.headers)["properties"]["periods"][0]

        #save the forecast in lowercase
        self.weather = self.forecast_data["shortForecast"].lower()
        return self.weather

    def get_weather(self,coords = [32.9004,-105.9629]):
        return self.forecast_from_gridpoints(self.coords_to_gridpoints(coords))
    

#create an instance of class = object
weather = Get_weather()
weather.get_weather()
