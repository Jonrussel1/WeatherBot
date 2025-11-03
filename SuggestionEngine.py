class SuggestionEngine:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, description, category):
        """Add a new task to the task list"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'category': category,  # 'indoor' or 'outdoor'
            'completed': False
        }
        self.tasks.append(task)
        return task
    
    def get_incomplete_tasks(self):
        """Get all tasks that aren't completed"""
        return [task for task in self.tasks if not task['completed']]
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                return True
        return False
    
    def generate_suggestions(self, weather_data):
        """Generate suggestions based on weather data"""
        suggestions = []
        incomplete_tasks = self.get_incomplete_tasks()
        
        # Extract weather information
        conditions = weather_data['conditions']
        temp = weather_data['temperature']
        description = weather_data['description'].lower()
        
        # General weather recommendations
        if temp < 50:
            suggestions.append("❄️ Wear a warm coat today")
        elif temp > 85:
            suggestions.append("☀️ Stay hydrated and wear sunscreen")
        elif temp > 75:
            suggestions.append("😎 Perfect weather for outdoor activities!")
        
        if any(word in conditions for word in ['rain', 'snow', 'thunderstorm']):
            suggestions.append("🌧️ Bring an umbrella or rain jacket")
        elif 'clear' in conditions:
            suggestions.append("✨ Beautiful clear day ahead!")
        
        if weather_data['wind_speed'] > 15:
            suggestions.append("💨 It's windy today - secure loose items")
        
        # Task-specific suggestions
        outdoor_tasks = [task for task in incomplete_tasks if task['category'] == 'outdoor']
        indoor_tasks = [task for task in incomplete_tasks if task['category'] == 'indoor']
        
        # Good weather for outdoor tasks
        if any(word in conditions for word in ['clear', 'clouds']) and not any(word in conditions for word in ['rain', 'snow', 'thunderstorm']):
            if outdoor_tasks and temp > 55 and temp < 90:
                suggestions.append("🌤️ Great day for outdoor tasks!")
                for task in outdoor_tasks[:3]:
                    suggestions.append(f"   ✓ Consider: {task['description']}")
        
        # Bad weather - suggest indoor tasks
        elif any(word in conditions for word in ['rain', 'snow', 'thunderstorm']):
            if indoor_tasks:
                suggestions.append("🏠 Better to focus on indoor activities")
                for task in indoor_tasks[:3]:
                    suggestions.append(f"   ✓ Good time for: {task['description']}")
        
        # If no specific suggestions, provide general ones
        if len(suggestions) <= 2:  # Only has basic weather suggestions
            if not incomplete_tasks:
                suggestions.append("📝 Add some tasks to get personalized suggestions!")
            else:
                suggestions.append("📊 Check your tasks for weather-appropriate activities")
        
        return suggestions
    
    def get_all_tasks(self):
        """Return all tasks"""
        return self.tasks