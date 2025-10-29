from tkinter import *
import tkinter as tk





  

class Suggestion_Window(Tk):
    def __init__(self):
        super().__init__()
    
        self.title('Suggestions')
        self.geometry("800x600")
        self.configure(bg='teal')
        

        self.lbl_frme_rec = LabelFrame(self, padx=10, pady=10)
        self.lbl_frme_rec.pack(pady=20)
        self.lbl_frme_rec.config(text=self.generate_suggestions)
        #labelFrames for each item...



    def generate_suggestions(self):
        self.current_weather = []#pull json keyword data like sunny, cloudy, etc
        if self.current_weather is 'sunny':
            self.label_r1 = Label(self, text='You should try...f{}')#generate random sunny suggestion from txt
            self.label_r1.pack(padx=15,pady=15)

""" def _add_weather_recommendations(self, condition):
        Add general weather-based recommendations
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
     #   Add suggestions based on tasks and weather compatibility
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

    def _add_default_suggestions(self):
    #Add default suggestions when no tasks are available
        self.good_cond = ["clear", "sunny", "clouds", "partly cloudy"]
        self.bad_cond = ["rain", "snow", "storm", "thunderstorm"]
        self.condition = []
        if any(self.good_cond in self.condition for self.good_cond in self.good_cond):
            self.label_show1 = Label(text="Perfect weather for outdoor activities")
            self.label_show1.pack(pady=60)

        elif any(bad_cond in self.condition for bad_cond in self.bad_cond):
            self.label_show2 = Label(text="Good day for indoor tasks and relaxation")
            self.label_show2.pack(pady=60)
        else:
            self.label_show3 = Label(text="Add tasks to get weather-specific suggestions!")
            self.label_show3.pack(pady=60)

    
    def get_quick_suggestion(self, weather_condition):
        
        
        
        
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
            """
        
#instantiation
app = Suggestion_Window()

app.mainloop()