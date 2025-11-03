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
        weather_text = weather_data[0].lower() if isinstance(weather_data, tuple) else str(weather_data).lower()
        temp = weather_data[1] if isinstance(weather_data, tuple) and len(weather_data) > 1 else None
        
        # General weather recommendations
        if temp is not None:
            if temp < 50:
                suggestions.append("Wear a warm coat today")
            elif temp > 80:
                suggestions.append("Stay hydrated and wear sunscreen")
        
        if any(word in weather_text for word in ['rain', 'shower', 'storm', 'precip']):
            suggestions.append("Bring an umbrella or rain jacket")
        
        if any(word in weather_text for word in ['sunny', 'clear', 'sun']):
            suggestions.append("Don't forget your sunglasses")
        
        # Task-specific suggestions
        outdoor_tasks = [task for task in incomplete_tasks if task['category'] == 'outdoor']
        indoor_tasks = [task for task in incomplete_tasks if task['category'] == 'indoor']
        
        # Good weather for outdoor tasks
        if any(word in weather_text for word in ['sunny', 'clear', 'partly', 'cloud']) and not any(word in weather_text for word in ['rain', 'storm']):
            if outdoor_tasks:
                suggestions.append("Great day for outdoor tasks!")
                for task in outdoor_tasks[:3]:  # Show first 3 outdoor tasks
                    suggestions.append(f"   ✓ Consider: {task['description']}")
        
        # Bad weather - suggest indoor tasks
        elif any(word in weather_text for word in ['rain', 'storm', 'snow', 'thunder']):
            if indoor_tasks:
                suggestions.append("Better to focus on indoor activities")
                for task in indoor_tasks[:3]:  # Show first 3 indoor tasks
                    suggestions.append(f"   ✓ Good time for: {task['description']}")
        
        # If no specific suggestions, provide general ones
        if not suggestions:
            suggestions.append("No specific suggestions. Check your tasks and weather!")
        
        return suggestions
    
    def get_all_tasks(self):
        """Return all tasks"""
        return self.tasks