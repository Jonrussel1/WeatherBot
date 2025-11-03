class SuggestionEngine:
    def __init__(self):
        self.suggestions = []
    
    def generate_suggestions(self, weather_data, task_manager=None):
        # Generate suggestions on task and weather data
        self.suggestions = []
        
        # Extract data from the real weather response
        conditions = weather_data['conditions']
        temp = weather_data['temperature']
        description = weather_data['description'].lower()
        wind_speed = weather_data.get('wind_speed', 0)
        humidity = weather_data.get('humidity', 50)
        
        # Weather-based suggestions using REAL data
        self._add_weather_suggestions(conditions, temp, wind_speed, humidity)
        
        # Task-based suggestions if task manager is provided
        if task_manager:
            self._add_task_suggestions(conditions, temp, task_manager)
        else:
            self._add_default_suggestions(conditions)
        
        return self.suggestions
    
    def _add_weather_suggestions(self, conditions, temp, wind_speed, humidity):
        # Add suggestions based on weather data
        # Temperature-based suggestions
        if temp < 32:
            self.suggestions.append("FREEZING temperatures - bundle up!")
            self.suggestions.append("Wear heavy coat, gloves, and hat")
        elif temp < 50:
            self.suggestions.append("Chilly day - wear a warm jacket")
        elif temp > 85:
            self.suggestions.append("Hot day - stay hydrated and seek shade")
            if humidity > 70:
                self.suggestions.append("High humidity - extra hydration needed")
        elif temp > 75:
            self.suggestions.append("Warm and pleasant - perfect outdoor weather")
        
        # Weather condition suggestions
        if any(word in conditions for word in ["rain", "drizzle"]):
            self.suggestions.append("Rain expected - bring umbrella/raincoat")
            self.suggestions.append("Drive carefully - wet roads")
        
        if "thunderstorm" in conditions:
            self.suggestions.append("THUNDERSTORM warning - avoid outdoor activities")
            self.suggestions.append("Stay indoors and away from windows")
        
        if "snow" in conditions:
            self.suggestions.append("Snow today - wear boots and warm layers")
            if temp > 32:
                self.suggestions.append("Wet snow - roads may be slippery")
        
        if wind_speed > 15:
            self.suggestions.append("Windy conditions - secure outdoor items")
        if wind_speed > 25:
            self.suggestions.append("Very windy - be cautious outdoors")
        
        if "clear" in conditions and temp > 65:
            self.suggestions.append("Perfect clear day - great for outdoor activities!")
    
    def _add_task_suggestions(self, conditions, temp, task_manager):
        # Add suggestions based on user tasks and weather data
        outdoor_tasks = task_manager.get_tasks_by_category("outdoor")
        indoor_tasks = task_manager.get_tasks_by_category("indoor")
        
        # Optimal outdoor conditions
        is_good_outdoor = (
            any(word in conditions for word in ["clear", "clouds"]) and 
            not any(word in conditions for word in ["rain", "snow", "thunderstorm"]) and
            temp >= 55 and temp <= 85 and
            "extreme" not in conditions
        )
        
        # Good weather for outdoor tasks
        if is_good_outdoor and outdoor_tasks:
            self.suggestions.append("EXCELLENT conditions for outdoor tasks:")
            for task in outdoor_tasks[:3]:
                self.suggestions.append(f"{task['description']}")
        
        # Bad weather for outdoor tasks
        elif any(word in conditions for word in ["rain", "snow", "thunderstorm"]) and indoor_tasks:
            self.suggestions.append("Perfect weather for indoor tasks:")
            for task in indoor_tasks[:3]:
                self.suggestions.append(f"{task['description']}")
        
        # Marginal outdoor conditions
        elif outdoor_tasks and (temp < 50 or temp > 85):
            self.suggestions.append("Challenging conditions for outdoor tasks:")
            for task in outdoor_tasks[:2]:
                self.suggestions.append(f"{task['description']} (dress appropriately)")
    
    def _add_default_suggestions(self, conditions):
        # Default suggestions if no task is added
        if any(word in conditions for word in ["clear", "clouds"]):
            self.suggestions.append("Add outdoor tasks to get activity suggestions!")
        elif any(word in conditions for word in ["rain", "storm", "snow"]):
            self.suggestions.append("Add indoor tasks for bad weather ideas!")
        else:
            self.suggestions.append("Add tasks to get personalized recommendations!")
    
    def get_quick_tip(self, weather_data):
        # Quick weather tip based on data
        conditions = weather_data['conditions']
        temp = weather_data['temperature']
        
        if "thunderstorm" in conditions:
            return "Storm warning - stay indoors!"
        elif "rain" in conditions:
            return "Rainy day - bring umbrella"
        elif "snow" in conditions:
            return "Snow today - dress warm"
        elif temp > 85:
            return "Hot! Stay hydrated"
        elif temp < 32:
            return "Freezing! Bundle up"
        elif "clear" in conditions and temp > 65:
            return "Perfect day for outdoors!"
        else:
            return "Check suggestions for today's plan"
