class SuggestionEngine:
    def __init__(self):
        self.suggestions = []
    
    def generate_suggestions(self, weather_data, task_manager=None):
        self.suggestions = []
    
        if not weather_data:
            self.suggestions.append("Please get weather data first to see personalized suggestions!")
            return self.suggestions    
        
        conditions = weather_data.get('conditions', '').lower()
        temp = weather_data.get('temperature', 72)
        description = weather_data.get('description', '').lower()
        
        # Weather-based suggestions
        self._add_weather_suggestions(conditions, temp, description)
        
        # Task-based suggestions
        if task_manager:
            self._add_task_suggestions(conditions, temp, task_manager)
        else:
            self.suggestions.append("Add tasks to get personalized activity recommendations!")
        
        # General activity suggestions based on just weather
        self._add_general_activity_suggestions(conditions, temp)

        return self.suggestions
    
    # Function will suggest clothing and weather-related advice
    def _add_weather_suggestions(self, conditions, temp, description):
        if temp < 32:
            self.suggestions.append("FREEZING - Bundle up with heavy coat!")
        elif temp < 50:
            self.suggestions.append("Chilly - Wear a warm jacket")
        elif temp > 85:
            self.suggestions.append("Hot day - Stay hydrated")
        
        # Weather condition suggestions
        if any(word in conditions for word in ["rain", "drizzle"]):
            self.suggestions.append("Rain expected - Bring umbrella")
        if "snow" in conditions:
            self.suggestions.append("Snow today - Wear boots")
        if "clear" in conditions and temp > 65:
            self.suggestions.append("Perfect clear day for outdoor activities!")
    
    def _add_task_suggestions(self, conditions, temp, task_manager):
        outdoor_tasks = task_manager.get_tasks_by_category("outdoor")
        indoor_tasks = task_manager.get_tasks_by_category("indoor")
        
        is_good_outdoor = ("clear" in conditions or "sunny" in conditions) and 55 <= temp <= 85
        
        if is_good_outdoor and outdoor_tasks:
            self.suggestions.append("GREAT for outdoor tasks:")
            for task in outdoor_tasks[:2]:
                self.suggestions.append(f"{task['description']}")
        
        if any(word in conditions for word in ["rain", "snow"]) and indoor_tasks:
            self.suggestions.append("Perfect for indoor tasks:")
            for task in indoor_tasks[:2]:
                self.suggestions.append(f"{task['description']}")

    # Function will suggest activities if no tasks are present
    def _add_general_activity_suggestions(self, conditions, temp):
        self.suggestions.append("Suggested Activities:")
        
        if any(word in conditions for word in ["clear", "sunny", "fair"]):
            if 60 <= temp <= 80:
                self.suggestions.append("   Perfect for walking, hiking, or outdoor sports")
                self.suggestions.append("   Great day for gardening or yard work")
                self.suggestions.append("   Consider a picnic or outdoor dining")
            elif temp > 80:
                self.suggestions.append("Good for swimming or water activities")
                self.suggestions.append("Visit air-conditioned spaces like museums")
        
        if any(word in conditions for word in ["rain", "drizzle"]):
            self.suggestions.append("   Visit museums, libraries, or indoor shopping")
            self.suggestions.append("   Perfect for reading, movies, or indoor hobbies")
            self.suggestions.append("   Great day for cooking or baking")
        
        if any(word in conditions for word in ["snow"]):
            self.suggestions.append("   Good for skiing, sledding, or building a snowman")
            self.suggestions.append("   Perfect for hot drinks and cozy indoor activities")
        
        if any(word in conditions for word in ["cloudy", "overcast"]):
            self.suggestions.append("   Comfortable for walking or light outdoor work")
            self.suggestions.append("   Good day for running errands or shopping")