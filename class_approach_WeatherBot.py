from tkinter import *
import os
import Weather


#class approach calls window by organizing data in a class...
class Weather_Main_Window(Tk):
    
    def __init__(self):
        super().__init__()
        # to get the location of the current python file
        self.basedir = os.path.dirname(os.path.abspath(__file__))

        #title, icon, size
        self.title('WeatherBot')
        self.geometry("800x600")
        self.configure(bg='teal')
        self.weather = Weather.Get_Weather()
       

        #label
        self.my_label = Label(self, text='Welcome to WeatherBot', font=('Helvetica', 42))
        self.my_label.pack(pady=20)
        self.Suggestion_button()
        self.Setting_Button()
        self.Todo_Button()
        self.Weather_Button()
        self.Exit_button()
    
    
    def Weather_Button(self):
        self.weather_button = Button(self, text="Get Weather Info", command=self.Open_Weather_Window, bg="#333", fg="white", bd=0)
        self.weather_button.pack(pady=30)
        
    def Todo_Button(self):
        self.todo_button = Button(self, text='To Do list', command=self.Open_ToDo_Window, bg='#333',fg='white',bd=0)
        self.todo_button.pack(pady=50)
    
    def Setting_Button(self):
        self.img = PhotoImage(file=self.basedir+"/gear.png").subsample(3, 3)
        self.menu = Menu(self, tearoff=0, bg="red", fg="black")
        self.setting_button = Button(self, image=self.img, bd=0, relief="flat", highlightthickness=0,
                bg="teal", activebackground="teal", command=self.Open_Settings_Window)
        self.setting_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
   
    def Get_Weather(self, coords):
        return self.weather.get_weather(coords)
    
    def Suggestion_button(self):
        self.suggest_button = Button(self, text='Recommend',command=self.Open_Suggestion_Window,bg='#333',fg='white',bd=0)
        self.suggest_button.pack(pady=60)
 
    def Exit_button(self):
        self.exit_button = Button(self, text='Exit',command=self.destroy, bg='#333',fg='white',bd=0)
        self.exit_button.pack(pady=65)
    
    def Open_Weather_Window(self):
        Weather_Window(self)
    def Open_ToDo_Window(self):
        Todo_Window(self)
    def Open_Settings_Window(self):
        Setting_Window(self)
        
    def Open_Suggestion_Window(self):
        Suggestion_Window(self)
class Weather_Window(Toplevel):
   
    def __init__(self, master): 
        super().__init__(master)

        self.master = master
        #title, icon, size
        self.title('Weather information')
        self.geometry("800x600")
        self.configure(bg='teal')
        
        self.my_label = Label(self, text='Weather Info', font=('Helvetica', 42))
        self.my_label.pack(pady=20)

        self.start_button()
        

    def start_button(self):
        self.start_btn = Button(self, text="Start", command=self.show_searchbar, bg="#333", fg="white", bd=0)
        self.start_btn.pack()

    def show_searchbar(self):
        self.start_btn.destroy()  # or: start_btn.pack_forget()
        self.topbar = Frame(self, bg="teal")
        self.topbar.pack(side="top", fill="x")
        q = StringVar()
        Entry(self.topbar, textvariable=q, font=("TkDefaultFont",12)).pack(side="left", padx=8, pady=8, fill="x", expand=True)
        Button(self.topbar, text="Search", bg="#333", fg="white", bd=0,
              command=lambda: q.set(self.master.Get_Weather(self.my_label.cget("text")))).pack(side="left", padx=6)
    
    
class Todo_Window(Toplevel):
    
    def __init__(self, master): 
        
        super().__init__(master)

        
         #title, icon, size
        self.title('To Do list')
        self.geometry("800x600")
        self.configure(bg='teal')


class Setting_Window(Toplevel):
    
    def __init__(self, master):
        super().__init__(master)
     
        self.title('Settings')
        self.geometry('400x400')
        self.setting_label = Label(self,text='Settings',font=('Helvetica', 20)).pack(anchor='w', padx=10)
    
        self.Sliders("Master")
        self.Sliders("Music")
        self.Sliders("SFX")
    
    def Sliders(self,name):
        self.slider_label = Label(self,text=name).pack(anchor='w',padx=10)
        self.Slider = Scale(self,from_=0, to=100, orient="horizontal")
        self.Slider.set(value=10)
        self.Slider.pack(padx=10, pady=2, fill="x")

class Suggestion_Window(Toplevel):
    
    def __init__(self, master):

        super().__init__()
            #title, icon, size
        self.title('Recommendations')
        self.geometry("800x600")
        self.configure(bg='teal')
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



        


#instantiation
app = Weather_Main_Window()





app.mainloop()