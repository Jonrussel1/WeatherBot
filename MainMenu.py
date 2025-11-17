from tkinter import *
import os
from Weather import Get_Weather
from TaskManager import TaskManager
from SuggestionEngine import SuggestionEngine
from Setting_Window import Setting_Window
from Suggestion_Window import Suggestion_Window
from Todo_Window import Todo_Window
from Weather_Window import Weather_Window
from PIL import Image, ImageTk

#class approach calls window by organizing data in a class...
class Weather_Main_Window(Tk):
    
    def __init__(self):
        super().__init__()
        # to get the location of the current python file
        self.basedir = os.path.dirname(os.path.abspath(__file__))

        #title, icon, size
        self.title('WeatherBot')
        self.geometry("800x600")
   
        
        self.weather = Get_Weather()
        self.forecast = "No Forecast"
        self.current_weather_data = None

        #initialize suggestion engine and task manager
        self.suggestion_engine = SuggestionEngine() 
        self.task_manager = TaskManager()
   

          


    

        #label
        self.my_label = Label(self, text='Welcome to WeatherBot')
        self.my_label.config(font=("Helvetica", 46, "bold"), fg="dark blue")
        
        self.my_label.config(highlightthickness=3, padx=4, pady=2)
        self.my_label.pack(pady=20)
        

        self.Suggestion_button()
        self.Setting_Button()
        self.Todo_Button()  
        
        self.Weather_Button()
      
        self.Exit_button()
        
        self.background_image()
        self.my_label.lift()
        self.suggest_button.lift()
        self.setting_button.lift()
        self.todo_button.lift()
        self.weather_button.lift()
        self.exit_button.lift()
    
        
    def background_image(self):
        self.imgzero = Image.open("clouds0.png")
        self.imgresize = self.imgzero.resize((800,600))
            
        self.img = ImageTk.PhotoImage(self.imgresize)
            
        self.labelzero = Label(image=self.img).place(x=0, y=0)
   
         
    
    def Weather_Button(self):
        self.weather_button = Button(self, text="Get Weather Info", command=self.Open_Weather_Window, bg="#333", fg="white", bd=0)
        self.weather_button.pack(pady=16)
        
        self.weather_button.configure(
            font=("Helvetica", 14, "bold"),
            bg="#0ea5e9", fg="white",
            activebackground="#0284c7", activeforeground="white",
            bd=0, relief="flat", padx=16, pady=10, cursor="hand2",
            highlightthickness=2, highlightbackground=self["bg"], highlightcolor="#38bdf8"
        )
        # cool hover effect (using in all buttons why not)
        self.weather_button.bind("<Enter>", lambda e: e.widget.configure(bg="#0284c7"))
        self.weather_button.bind("<Leave>", lambda e: e.widget.configure(bg="#0ea5e9"))
        
    def Todo_Button(self):
        self.todo_button = Button(self, text='To Do List', command=self.Open_ToDo_Window, bg='#333',fg='white',bd=0)
        self.todo_button.pack(pady=50)
    
    def Setting_Button(self):
        # keep the gear icon usage (ensure gear.png exists in the same folder)
        try:
            self.img = PhotoImage(file=self.basedir + "/gear3.png").subsample(3, 3)
        except Exception:
            self.img = None
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
        self.exit_button = Button(self, text='Exit', command=self.destroy, bg='#333', fg='white', bd=0)
        self.exit_button.pack(pady=16)  # redid packing it was sitting behind png icon
        self.exit_button.configure(
            font=("Helvetica", 14, "bold"),
            bg="#ef4444", fg="white",
            activebackground="#dc2626", activeforeground="white",
            bd=0, relief="flat", padx=16, pady=10, cursor="hand2",
            highlightthickness=2, highlightbackground=self["bg"], highlightcolor="#fecaca"
        )
        self.exit_button.bind("<Enter>", lambda e: e.widget.configure(bg="#dc2626"))
        self.exit_button.bind("<Leave>", lambda e: e.widget.configure(bg="#ef4444"))
    
    

    def Open_Weather_Window(self):
        Weather_Window(self)

    def Open_ToDo_Window(self):
        Todo_Window(self)

    def Open_Settings_Window(self):
        Setting_Window(self) 

    def Open_Suggestion_Window(self):
        Suggestion_Window(self)

            

#instantiation
app = Weather_Main_Window()
app.mainloop()