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
import tkinter.font as tkFont
import pyglet as pg

#class approach calls window by organizing data in a class...
class Weather_Main_Window(Tk):
    
    def __init__(self):
        super().__init__()
        # to get the location of the current python file
        self.basedir = os.path.dirname(os.path.abspath(__file__))

        #title, icon, size
        self.title('WeatherBot')
        self.geometry('3840x2160')
        self.config()
   
        
        self.weather = Get_Weather()
        self.forecast = "No Forecast"
        self.current_weather_data = None

        self.suggestion_engine = SuggestionEngine() 
        self.task_manager = TaskManager()
   
        self.cf = pg.font.add_file('anda.ttf')
        self.my_label = Label(self, text='Welcome to WeatherBot') 
        self.my_label.config(font=("cf", 46, "bold"))
        self.my_label.pack(pady=20)
        
    
        


       
        
      

        

        

        self.Weather_Button()
        self.Setting_Button()
        self.Todo_Button()  
        
        self.Suggestion_button()
      
        self.Exit_button()
        
        self.background_image()
        self.my_label.lift()
        self.suggest_button.lift()
        self.setting_button.lift()
      
        self.todo_button.lift()
        self.weather_button.lift()
        self.exit_button.lift()
    
    #image for background...
    def background_image(self):
        self.imgzero = Image.open("clouds0.png")
        self.imgresize = self.imgzero.resize((3840,2160))
        self.img = ImageTk.PhotoImage(self.imgresize)
        self.labelzero = Label(image=self.img).place(x=0, y=0)
   
         
    
    def Weather_Button(self):
        # weather button bigger (larger font + larger padding)
        self.weather_button = Button(self, text="Get Weather Info", command=self.Open_Weather_Window, bg="#8dbbdc", fg="#f8fbff", bd=0)
        self.weather_button.pack(pady=20)
        
        self.weather_button.configure(
            font=("Helvetica", 18, "bold"),
            bg="#8dbbdc", fg="#f8fbff",
            activebackground="#6fa8cc", activeforeground="#f8fbff",
            bd=0, relief="flat", padx=24, pady=14, cursor="hand2",
            highlightthickness=2, highlightbackground=self["bg"], highlightcolor="#cfeaf8"
        )
        # soft hover effect
        self.weather_button.bind("<Enter>", lambda e: e.widget.configure(bg="#6fa8cc"))
        self.weather_button.bind("<Leave>", lambda e: e.widget.configure(bg="#8dbbdc"))
        
    def Todo_Button(self):
        # even padding for all secondary buttons
        self.todo_button = Button(self, text='To Do List', command=self.Open_ToDo_Window, bg='#a7c7e7', fg='#1f2b33', bd=0)
        self.todo_button.pack(pady=20)

        self.todo_button.configure(
            font=("Helvetica", 14, "bold"),
            bg="#a7c7e7", fg="#1f2b33",
            activebackground="#90b8dd", activeforeground="#1f2b33",
            bd=0, relief="flat", padx=24, pady=14, cursor="hand2",
            highlightthickness=2, highlightbackground=self["bg"], highlightcolor="#d9e9f6"
        )
        # soft hover effect
        self.todo_button.bind("<Enter>", lambda e: e.widget.configure(bg="#90b8dd"))
        self.todo_button.bind("<Leave>", lambda e: e.widget.configure(bg="#a7c7e7"))
    
    def Setting_Button(self):
        # keep the gear icon usage (ensure gear.png exists in the same folder)
        try:
            self.sett_img = PhotoImage(file=self.basedir + "/gear3.png").subsample(3, 3)
        except Exception:
            self.sett_img = None
        self.menu = Menu(self, tearoff=0, bg="red", fg="black")
        # neutral light background that matches misty palette
        self.setting_button = Button(self, image=self.sett_img, bd=0, relief="flat", highlightthickness=0,
                                     bg="#e0e7eb", activebackground="#e0e7eb", command=self.Open_Settings_Window)
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
        # even padding for all secondary buttons
        self.suggest_button = Button(self, text='Suggestions', command=self.Open_Suggestion_Window, bg='#a7c7e7', fg='#1f2b33', bd=0)
        self.suggest_button.pack(pady=20)

        self.suggest_button.configure(
            font=("Helvetica", 14, "bold"),
            bg="#a7c7e7", fg="#1f2b33",
            activebackground="#90b8dd", activeforeground="#1f2b33",
            bd=0, relief="flat", padx=24, pady=14, cursor="hand2",
            highlightthickness=2, highlightbackground=self["bg"], highlightcolor="#d9e9f6"
        )
        # soft hover effect
        self.suggest_button.bind("<Enter>", lambda e: e.widget.configure(bg="#90b8dd"))
        self.suggest_button.bind("<Leave>", lambda e: e.widget.configure(bg="#a7c7e7"))
 
    def Exit_button(self):
        # even padding for all secondary buttons
        self.exit_button = Button(self, text='Exit', command=self.destroy, bg='#6c7a89', fg='#f8fbff', bd=0)
        self.exit_button.pack(pady=20)  # redid packing it was sitting behind png icon
        self.exit_button.configure(
            font=("Helvetica", 14, "bold"),
            bg="#6c7a89", fg="#f8fbff",
            activebackground="#55656f", activeforeground="#f8fbff",
            bd=0, relief="flat", padx=24, pady=14, cursor="hand2",
            highlightthickness=2, highlightbackground=self["bg"], highlightcolor="#c6d3de"
        )
        self.exit_button.bind("<Enter>", lambda e: e.widget.configure(bg="#55656f"))
        self.exit_button.bind("<Leave>", lambda e: e.widget.configure(bg="#6c7a89"))
    
    

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
