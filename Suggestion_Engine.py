"""
Suggestion Engine Module for WeatherBot
Integrated with main WeatherBot coordinate system and tkinter interface.
"""

class SuggestionEngine:
    def __init__(self):
        self.suggestions = []

    def generate_suggestions(self, weather_condition, task_list=None):
        """
        Generate suggestions based on weather conditions from main Weather module.

        Args:
            weather_condition (str): Weather description from Weather.get_weather()
            task_list (list): List of task dictionaries (optional for now)

        Returns:
            list: List of suggestion strings ready for tkinter display
        """
        self.suggestions = []

        # Convert weather condition to lowercase for consistent checking
        condition = weather_condition.lower() if weather_condition else ""

        # Add general weather recommendations based on condition
        self._add_weather_recommendations(condition)

        # Add task-specific suggestions if tasks are provided
        if task_list:
            self._add_task_suggestions(condition, task_list)
        else:
            # Default suggestions when no tasks are available
            self._add_default_suggestions(condition)

        return self.suggestions

    def _add_weather_recommendations(self, condition):
        """Add general weather-based recommendations"""
        try:
            # Rain-related conditions
            rain_conditions = ["rain", "drizzle", "storm", "thunderstorm"]
            if any(rain_word in condition for rain_word in rain_conditions):
                self.suggestions.append("Bring an umbrella or rain jacket")

            # Cold conditions
            cold_conditions = ["snow", "ice", "freezing", "cold"]
            if any(cold_word in condition for cold_word in cold_conditions):
                self.suggestions.append("Wear warm clothing and layers")

            # Hot/sunny conditions
            hot_conditions = ["sunny", "clear", "hot"]
            if any(hot_word in condition for hot_word in hot_conditions):
                self.suggestions.append("Wear sunscreen and stay hydrated")

            # Windy conditions
            if "wind" in condition:
                self.suggestions.append("It's windy - secure loose items")

        except Exception as e:
            print(f"Error in weather recommendations: {e}")
            self.suggestions.append("Check weather conditions for today")

    def _add_task_suggestions(self, condition, task_list):
        """Add suggestions based on tasks and weather compatibility"""
        try:
            # Filter incomplete tasks
            incomplete_tasks = [task for task in task_list if not task.get('completed', False)]

            # Good weather for outdoor tasks
            good_outdoor_conditions = ["clear", "sunny", "clouds", "partly cloudy", "fair"]
            if any(good_cond in condition for good_cond in good_outdoor_conditions):
                outdoor_tasks = [task for task in incomplete_tasks 
                               if task.get('category', '').lower() == 'outdoor']

                if outdoor_tasks:
                    self.suggestions.append("Great day for outdoor tasks!")
                    for task in outdoor_tasks[:2]:  # Limit to 2 suggestions
                        self.suggestions.append(f"   ✓ {task.get('description', '')}")

            # Bad weather - suggest indoor tasks
            bad_weather_conditions = ["rain", "snow", "storm", "thunderstorm"]
            if any(bad_cond in condition for bad_cond in bad_weather_conditions):
                indoor_tasks = [task for task in incomplete_tasks 
                              if task.get('category', '').lower() == 'indoor']

                if indoor_tasks:
                    self.suggestions.append("Better for indoor activities")
                    for task in indoor_tasks[:2]:  # Limit to 2 suggestions
                        self.suggestions.append(f"   ✓ {task.get('description', '')}")

        except Exception as e:
            print(f"Error in task suggestions: {e}")

    def _add_default_suggestions(self, condition):
        """Add default suggestions when no tasks are available"""
        good_conditions = ["clear", "sunny", "clouds", "partly cloudy"]
        bad_conditions = ["rain", "snow", "storm", "thunderstorm"]

        if any(good_cond in condition for good_cond in good_conditions):
            self.suggestions.append("Perfect weather for outdoor activities")
            self.suggestions.append("Add tasks to get personalized suggestions!")
        elif any(bad_cond in condition for bad_cond in bad_conditions):
            self.suggestions.append("Good day for indoor tasks and relaxation")
            self.suggestions.append("Add tasks to get personalized suggestions!")
        else:
            self.suggestions.append("Add tasks to get weather-specific suggestions!")

    def get_quick_suggestion(self, weather_condition):
        """
        Get a single, high-priority suggestion for the main display

        Returns:
            str: Single most important suggestion
        """
        if not weather_condition:
            return "Enter coordinates to get weather suggestions"

        condition = weather_condition.lower()

        if any(word in condition for word in ["rain", "storm", "drizzle"]):
            return "Rain expected - bring umbrella"
        elif any(word in condition for word in ["snow", "ice", "freezing"]):
            return "Cold weather - dress warmly"
        elif any(word in condition for word in ["sunny", "clear", "hot"]):
            return "Sunny day - perfect for outdoors"
        elif any(word in condition for word in ["cloud", "overcast"]):
            return "Cloudy but good for activities"
        else:
            return "Check your tasks for today's plans"