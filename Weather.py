import requests

class WeatherAPI:
    def __init__(self):
        self.api_key = "fb8e60a12a00ddbc1d6c3f3b02f61728"  
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
    def get_weather_by_coords(self, lat, lon):
        # Get weather by coordinates
        try:
            # Input validation
            lat_clean = str(lat).strip()
            lon_clean = str(lon).strip()

            try:
                lat_num = float(lat_clean)
                lon_num = float(lon_clean)

                # Basic range check
                if not (-90 <= lat_num <= 90):
                    return self._get_error_weather("Latitude must be between -90 and 90.")
                if not (-180 <= lon_num <= 180):
                    return self._get_error_weather("Longitude must be between -180 and 180.")
            except ValueError:
                return self._get_error_weather("Coordinates must be valid numbers.")
                
            params = {
                'lat': lat_clean,
                'lon': lon_clean,
                'appid': self.api_key,
                'units': 'imperial'
            }
            
            print(f"Fetching weather for: {lat_clean}, {lon_clean}")

            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                weather_data = self._parse_weather_data(response.json())
                print(f"Weather data received: {weather_data['description']} at {weather_data['temperature']}°F in {weather_data['location']}")
                return weather_data
            else:
                error_msg = self._handle_api_error(response.status_code)
                print(f"API error: {error_msg}")
                return self._get_fallback_weather(lat_clean, lon_clean, error_msg)
                
        except Exception as e:
            print(f"Network error: {e}")
            return self._get_fallback_weather(lat, lon, str(e))
    
    def _parse_weather_data(self, data):
        # Extract relevant weather data
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Get location name - use what the API provides
        location_name = data.get('name', '')
        if not location_name:
            # If no name, use coordinates
            coord = data.get('coord', {})
            location_name = f"Location ({coord.get('lat', '?')},{coord.get('lon', '?')})"
        
        # Return data for suggestions
        return {
            'description': weather_desc,
            'temperature': temp,
            'feels_like': feels_like,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'location': location_name,
            'conditions': data['weather'][0]['main'].lower()
        }
    
    def _handle_api_error(self, status_code):
        # Handle different API error codes
        error_messages = {
            401: "Invalid API key.",
            404: "Location not found.",
            429: "API rate limit exceeded.",
            500: "Server error at weather service.",
            503: "Service unavailable at weather service."
        }
        return error_messages.get(status_code, f"API Error: {status_code}")
    
    def _get_fallback_weather(self, lat, lon, error_reason):
        # Provide fallback weather data if API fails
        print(f"Using fallback weather due to: {error_reason}")
        return {
            'description': 'Weather data unavailable',
            'temperature': 72,
            'feels_like': 72,
            'humidity': 50,
            'wind_speed': 5,
            'location': f"Location ({lat[:8]},{lon[:8]})",
            'conditions': 'unknown',
            'error': error_reason
        }
    
    def _get_error_weather(self, error_message):
        # Return error weather data
        return {
            'description': error_message,
            'temperature': 0,
            'feels_like': 0,
            'humidity': 0,
            'wind_speed': 0,
            'location': "Error",
            'conditions': error_message,
            'error': error_message
        }

def get_weather(coords):
    # Get weather information for given coordinates
    api = WeatherAPI()
    
    if isinstance(coords, str):
        coords = coords.split(',')
    
    if len(coords) == 2:
        weather_data = api.get_weather_by_coords(coords[0], coords[1])
        
        # Check for errors in weather data
        if 'error' in weather_data:
            error_msg = f"Error: {weather_data['error']}"
            print(f"Returning error: {error_msg}")
            return error_msg

        result = f"Current weather: {weather_data['description'].title()}\nTemperature: {round(weather_data['temperature'])}°F\nLocation: {weather_data['location']}"
        print(f"Returning weather data: {result}")
        return result        
    else:
        error_msg = "Error: Please use format: latitude,longitude"
        print(f"Format error: {error_msg}")
        return error_msg
    


