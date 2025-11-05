class SuggestionEngine:
    def __init__(self):
        self.suggestions = []
    
    def generate_suggestions(self, weather_data, task_manager=None):
        self.suggestions = []
        
        conditions = weather_data['conditions']
        temp = weather_data.get('temperature', 72)
        description = weather_data['description'].lower()
        
        # Weather-based suggestions
        self._add_weather_suggestions(conditions, temp)
        
        # Task-based suggestions
        if task_manager:
            self._add_task_suggestions(conditions, temp, task_manager)
        else:
            self._add_default_suggestions(conditions)
        
        return self.suggestions
    
    def _add_weather_suggestions(self, conditions, temp):
        if temp < 32:
            self.suggestions.append("FREEZING - Bundle up with heavy coat!")
        elif temp < 50:
            self.suggestions.append("Chilly - Wear a warm jacket")
        elif temp > 85:
            self.suggestions.append("Hot day - Stay hydrated")
        
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
    
    def _add_default_suggestions(self, conditions):
        if "clear" in conditions:
            self.suggestions.append("Add outdoor tasks for activity suggestions!")
        elif "rain" in conditions:
            self.suggestions.append("Add indoor tasks for rainy day ideas!")