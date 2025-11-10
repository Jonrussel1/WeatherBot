from tkinter import *
import os
import Weather
from TaskManager import TaskManager
from SuggestionEngine import SuggestionEngine

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
        self.forecast = "No Forecast"
        self.current_weather_data = None

        #initialize suggestion engine and task manager
        self.suggestion_engine = SuggestionEngine() 
        self.task_manager = TaskManager()

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
        self.todo_button = Button(self, text='To Do List', command=self.Open_ToDo_Window, bg='#333',fg='white',bd=0)
        self.todo_button.pack(pady=50)
    
    def Setting_Button(self):
        self.img = PhotoImage(file=self.basedir+"/gear.png").subsample(3, 3)
        self.menu = Menu(self, tearoff=0, bg="red", fg="black")
        self.setting_button = Button(self, image=self.img, bd=0, relief="flat", highlightthickness=0,
                bg="teal", activebackground="teal", command=self.Open_Settings_Window)
        self.setting_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
   
    def Get_Weather(self, coords):
        try:
            self.forecast = self.weather.get_weather(coords)
            self.current_weather_data = self.forecast
            return f"Current Weather: {self.forecast['weather'].title()} | Temperature: {self.forecast['temp']} | Location: {self.forecast['location']}"
        except:
            self.current_weather_data = None
            return "Invalid coordinates or weather data unavailable."
        
    
    def Suggestion_button(self):
        self.suggest_button = Button(self, text='Suggestions',command=self.Open_Suggestion_Window,bg='#333',fg='white',bd=0)
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
              command=lambda: q.set(self.master.Get_Weather(q.get()))).pack(side="left", padx=6)
    
    
class Todo_Window(Toplevel):
    
    def __init__(self, master): 
        super().__init__(master)
        self.master = master

        #title, icon, size
        self.title('Task Manager')
        self.geometry("600x400")
        self.configure(bg='teal')
        
        #Task input frame
        input_frame = Frame(self, bg='teal')
        input_frame.pack(pady=10)

        Label(input_frame, text='Task:', bg='teal', fg='white').pack(side='left')
        self.task_entry = Entry(input_frame, width=20, font=('Arial', 12))
        self.task_entry.pack(side='left', padx=5)

        self.category_var = StringVar(value="outdoor")
        Radiobutton(input_frame, text="Outdoor", variable=self.category_var, value="outdoor", bg='teal', fg='white', selectcolor='teal').pack(side="left")
        Radiobutton(input_frame, text="Indoor", variable=self.category_var, value="indoor", bg='teal', fg='white', selectcolor='teal').pack(side="left")
        
        Button(input_frame, text="Add Task", command=self.add_new_task).pack(side="left", padx=5)
        
        # Task list frame
        list_frame = Frame(self, bg='teal')
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        Label(list_frame, text="Your Tasks:", font=("Arial", 14, "bold"), bg='teal', fg='white').pack(anchor="w")
        
        self.task_list_frame = Frame(list_frame, bg='teal')
        self.task_list_frame.pack(fill="both", expand=True)
        
        self.update_task_list()
    
    def add_new_task(self):
        description = self.task_entry.get().strip()
        if description:
            self.master.task_manager.add_task(description, self.category_var.get())
            self.task_entry.delete(0, END)
            self.update_task_list()
    
    def update_task_list(self, show_completed=False):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        # Filter tasks based on show_completed flag
        if show_completed:
            tasks_to_show = self.master.task_manager.get_all_tasks()
        else:
            tasks_to_show = self.master.task_manager.get_incomplete_tasks()
    
        if not tasks_to_show:
            # Show appropriate empty message
            message = "No tasks to display!" if show_completed else "No active tasks - add some above!"
            empty_frame = Frame(self.task_list_frame, bg='teal')
            empty_frame.pack(fill="x", pady=10)
            Label(empty_frame, text=message, 
              fg="white", bg='teal', font=("Arial", 11, "italic")).pack()
            return
    
        for task in tasks_to_show:
            task_frame = Frame(self.task_list_frame, bg='teal')
            task_frame.pack(fill="x", pady=2)
        
            status = "✓" if task['completed'] else "○"
            color = "light gray" if task['completed'] else "white"
            task_text = f"{status} {task['description']} ({task['category']})"
        
            Label(task_frame, text=task_text, fg=color, bg='teal', font=("Arial", 11)).pack(side="left")
        
            if not task['completed']:
                Button(task_frame, text="Complete", command=lambda t=task: self.complete_task(t['id']), font=("Arial", 8)).pack(side="right")
            else:
                Button(task_frame, text="Delete", command=lambda t=task: self.delete_task(t['id']), font=("Arial", 8), bg="red").pack(side="right")
    
    def complete_task(self, task_id):
        self.master.task_manager.complete_task(task_id)
        self.update_task_list()

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
        super().__init__(master)
        self.master = master
        
        #title, icon, size
        self.title('Smart Suggestions')
        self.geometry("700x500")
        self.configure(bg='teal')
        
        Label(self, text="Smart Suggestions", font=('Helvetica', 20), bg='teal', fg='white').pack(pady=20)
        
        # Suggestions display
        self.suggestions_text = Text(self, wrap=WORD, width=60, height=15, font=("Arial", 12), bg='lightcyan')
        self.suggestions_text.pack(pady=10, padx=20, fill=BOTH, expand=True)
        
        # Refresh button
        Button(self, text="Refresh Suggestions", command=self.refresh_suggestions,font=("Arial", 12), bg='#00a0a0', fg='white').pack(pady=10)
        
        # Load initial suggestions
        self.refresh_suggestions()
    
    def refresh_suggestions(self):
        #Refresh suggestions based on current weather and tasks
        self.suggestions_text.delete(1.0, END)
        
        # Get current weather data for suggestions
        weather_data = self.get_weather_data_for_suggestions()
        
        if weather_data:
            # Generate suggestions using your SuggestionEngine
            suggestions = self.master.suggestion_engine.generate_suggestions(weather_data, self.master.task_manager)
            
            # Display suggestions
            if suggestions:
                for suggestion in suggestions:
                    self.suggestions_text.insert(END, f"• {suggestion}\n\n")
            else:
                self.suggestions_text.insert(END, "Get weather data and add tasks to see personalized suggestions!")
        else:
            self.suggestions_text.insert(END, "Please get weather data first to see suggestions!")
    
    def get_weather_data_for_suggestions(self):
        #Convert current weather to SuggestionEngine format
        try:
            if hasattr(self.master, 'forecast') and isinstance(self.master.forecast, dict):
                return {
                    'description': self.master.forecast.get('weather', '').lower(),
                    'temperature': self.master.forecast.get('temp', 72),
                    'conditions': self.master.forecast.get('weather', '').lower(),
                    'location': self.master.forecast.get('location', 'Current Location')
                }
            elif hasattr(self.master, 'forecast') and isinstance(self.master.forecast, dict):
                weather_data = self.master.forecast
            return {
                'description': weather_data.get('weather', '').lower(),
                'temperature': weather_data.get('temp', 72),
                'conditions': weather_data.get('weather', '').lower(),
                'location': weather_data.get('location', 'Current Location')
            }
        except Exception as e:
            print(f"Error getting weather data for suggestions: {e}")
        return None



        


#instantiation
app = Weather_Main_Window()




      
app.mainloop()













