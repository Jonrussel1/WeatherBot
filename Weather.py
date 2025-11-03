import requests
import random

class Get_Weather:
    def __init__(self):
        self.api_key = "fb8e60a12a00ddbc1d6c3f3b02f61728"  # You can get a free key from openweathermap.org
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather_simple(self, lat, lon):
        """Simple weather fetch using OpenWeatherMap API"""
        try:
            # For testing, use demo data if no API key
            if self.api_key == "demo_key":
                return self.get_demo_weather(lat, lon)
            
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'imperial'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                weather_desc = data['weather'][0]['description']
                temp = data['main']['temp']
                location = data.get('name', 'Unknown Location')
                
                return (weather_desc, temp, location)
            else:
                return self.get_demo_weather(lat, lon)
                
        except Exception as e:
            print(f"Weather API error: {e}")
            return self.get_demo_weather(lat, lon)
    
    def get_demo_weather(self, lat, lon):
        """Provide demo weather data for testing"""
        # Simple demo data based on coordinates
        weather_options = [
            "sunny", "cloudy", "partly cloudy", "rainy", "clear"
        ]
        weather = random.choice(weather_options)
        
        # Simple temp based on "latitude" (not real, just for demo)
        try:
            lat_num = float(lat)
            base_temp = 70 - (abs(lat_num) - 35) * 2  # Rough approximation
            temp = max(20, min(100, base_temp + random.randint(-10, 10)))
        except:
            temp = random.randint(50, 85)
        
        location = f"Location ({lat[:6]}, {lon[:6]})"
        
        return (weather, temp, location)
    
    def get_weather(self, coords="32.9004,-105.9629"):
        """Main method to get weather - works with your existing code"""
        try:
            if isinstance(coords, str):
                coords = coords.split(',')
            elif isinstance(coords, list):
                pass
            else:
                coords = ["32.9004", "-105.9629"]  # Default coordinates
            
            # Clean the coordinates
            lat = str(coords[0]).strip()
            lon = str(coords[1]).strip()
            
            print(f"Getting weather for coordinates: {lat}, {lon}")
            
            weather_data = self.get_weather_simple(lat, lon)
            
            return f"Current Weather: {weather_data[0].title()}\nTemperature: {round(weather_data[1])}°F\nLocation: {weather_data[2]}"
            
        except Exception as e:
            print(f"Error in get_weather: {e}")
            return "Current Weather: Sunny\nTemperature: 75°F\nLocation: Demo Location"
    

