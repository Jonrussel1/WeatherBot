from tkinter import *
import tkinter as tk
import requests
import pgeocode

class Get_Weather:
    """Class to get weather
    """
    def __init__(self):
        """Sets up api agent, and other permanent variables
        """
        super().__init__()
        #needed to access api
        self.user_agent = "WeatherBot"
        self.BASE_URL = "https://api.weather.gov"
        self.headers = {'User-Agent' : f'{self.user_agent}'}

    def get_data_as_json(self,endpoint, headers):
        """Is given web address and header, returns json of site

        Args:
            endpoint (string): Site to look at
            headers (string): Headers for site request

        Raises:
            Exception: Failed to Access site

        Returns:
            json: Json from site
        """
        self.response = requests.get(endpoint, headers = self.headers) #raise error if api failed
        if self.response:
            print("API accessed successfully.")
        else:
            raise Exception(f"Non-success status code: {self.response.status_code}")
        return self.response.json()


    def coords_to_gridpoints(self,coordinates):
        """Turns global coordinates into weather station gridpoints, as well as the location name

        Args:
            coordinates (tuple): Contains x and y coordinates 

        Returns:
            dict: Dictionary containing station id, gridpoint x and y, and the location name
        """
        #Creates link
        self.coordinate_endpoint = f"{self.BASE_URL}/points/{coordinates[0]},{coordinates[1]}"
        
        #Goes through json to get necessary data
        self.coordinate_data = self.get_data_as_json(self.coordinate_endpoint, self.headers)["properties"]
        self.location_data = self.coordinate_data["relativeLocation"]["properties"]
        self.location = f"{self.location_data['city']}, {self.location_data['state']}"
        
        #Puts data in dict
        self.station__coords_and_location = {"gridId":self.coordinate_data["gridId"], "x":self.coordinate_data["gridX"], "y":self.coordinate_data["gridY"], "location":self.location}
        return self.station__coords_and_location

    def forecast_from_gridpoints(self,station_and_coords):
        """Uses gridpoints to get forecast

        Args:
            station_and_coords (dict): Dictionary containing station id, gridpoint x and y, and the location name

        Returns:
            dict: Dictionary containing weather, temp, and location
        """
        #Create link
        self.forecast_endpoint = f"{self.BASE_URL}/gridpoints/{station_and_coords['gridId']}/{station_and_coords['x']},{station_and_coords['y']}/forecast"
        
        #Gets necessary data from json (current half of day, either 00-11 or 12-23)
        self.forecast_data = self.get_data_as_json(self.forecast_endpoint, self.headers)["properties"]["periods"][0]

        #Puts data in dict
        self.weather = self.forecast_data["shortForecast"].lower()
        self.temp = self.forecast_data["temperature"]
        return {"weather":self.weather, "temp":self.temp, "location":station_and_coords["location"]}

    def get_weather(self,zip = "88310"):
        """Takes zip code and returns weather dict

        Args:
            zip (str, optional): Zipcode for location. Defaults to "88310" which is Alamogordo NM.

        Returns:
            dict:  Dictionary containing weather, temp, and location
        """
        #Tells it that we are in US
        self.nomi = pgeocode.Nominatim('us')
        
        #Get data from US zip code, then gets the coordinates
        self.loc_data = self.nomi.query_postal_code(zip)
        self.coords = [float(self.loc_data["latitude"]),float(self.loc_data["longitude"])]
        
        #Get forecast using coordinates
        try:
            self.data = self.forecast_from_gridpoints(self.coords_to_gridpoints(self.coords))
        except:
            return f"Invalid zip code"

        return self.data
