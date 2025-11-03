import requests
import random

class Get_Weather:
    def __init__(self):
        # REPLACE THIS WITH YOUR ACTUAL API KEY
        self.api_key = "fb8e60a12a00ddbc1d6c3f3b02f61728"  
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather_data(self, lat, lon):
        """Get real weather data from OpenWeatherMap"""
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'imperial'  # Gets temperature in Fahrenheit
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_weather_data(data)
            else:
                print(f"API Error: {response.status_code}")
                return self.get_demo_weather(lat, lon)
                
        except Exception as e:
            print(f"Weather API error: {e}")
            return self.get_demo_weather(lat, lon)
    
    def _parse_weather_data(self, data):
        """Extract the important weather information"""
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        location = data.get('name', 'Unknown Location')
        
        # Return data for suggestions
        return {
            'description': weather_desc,
            'temperature': temp,
            'feels_like': feels_like,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'location': location,
            'conditions': data['weather'][0]['main'].lower()
        }
    
    def get_demo_weather(self, lat, lon):
        """Fallback demo data if API fails"""
        # Simple demo data based on coordinates
        weather_conditions = ['clear', 'clouds', 'rain', 'snow', 'thunderstorm']
        condition = random.choice(weather_conditions)
        
        # Map conditions to descriptions
        condition_descriptions = {
            'clear': 'clear sky',
            'clouds': 'scattered clouds', 
            'rain': 'light rain',
            'snow': 'light snow',
            'thunderstorm': 'thunderstorm'
        }
        
        try:
            lat_num = float(lat)
            base_temp = 70 - (abs(lat_num) - 35) * 2
            temp = max(20, min(100, base_temp + random.randint(-10, 10)))
        except:
            temp = random.randint(50, 85)
        
        location = f"Location ({lat[:6]}, {lon[:6]})"
        
        return {
            'description': condition_descriptions[condition],
            'temperature': temp,
            'feels_like': temp - random.randint(0, 5),
            'humidity': random.randint(30, 90),
            'wind_speed': random.randint(0, 15),
            'location': location,
            'conditions': condition
        }
    
    def get_weather(self, coords="40.7128,-74.0060"):
        """Main method to get weather - works with your existing code"""
        try:
            if isinstance(coords, str):
                coords = coords.split(',')
            
            # Clean the coordinates
            lat = str(coords[0]).strip()
            lon = str(coords[1]).strip()
            
            print(f"Getting weather for coordinates: {lat}, {lon}")
            
            weather_data = self.get_weather_data(lat, lon)
            
            # Format for display
            return f"Current Weather: {weather_data['description'].title()}\nTemperature: {round(weather_data['temperature'])}°F\nLocation: {weather_data['location']}"
            
        except Exception as e:
            print(f"Error in get_weather: {e}")
            return "Current Weather: Sunny\nTemperature: 75°F\nLocation: Demo Location"

