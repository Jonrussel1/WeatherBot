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
        self.my_label.config(font=("Helvetica", 36, "bold"), fg="white", bg=self["bg"])
        self.my_label.config(highlightthickness=3, padx=4, pady=2)
        self.my_label.pack(pady=20)
        self.Suggestion_button()
        self.Setting_Button()
        self.Todo_Button()
        self.Weather_Button()
        self.Exit_button()
    
    
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
            self.img = PhotoImage(file=self.basedir + "/gear.png").subsample(3, 3)
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

class Weather_Window(Toplevel):
   
    def __init__(self, master): 
        super().__init__(master)


class Weather_Window(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # window styling
        self.title('Weather information')
        self.geometry("800x600")
        self.configure(bg='teal')

        # --- Header ---
        self.header = Frame(self, bg='teal')
        self.header.pack(fill="x", pady=(18, 6))

        self.title_label = Label(
            self.header, text='Weather Info',
            font=('Helvetica', 30, 'bold'),
            fg='white', bg='teal'
        )
        self.title_label.pack()

        self.subtitle_label = Label(
            self.header,
            text='Search by ZIP or "lat, lon" to see current conditions',
            font=('Helvetica', 12),
            fg='#e0f2f1', bg='teal'
        )
        self.subtitle_label.pack(pady=(4, 0))

        # --- Content split ---
        self.content = Frame(self, bg='teal')
        self.content.pack(fill="both", expand=True, padx=24, pady=12)

        self.left = Frame(self.content, bg='teal')
        self.left.pack(side='left', fill='y', padx=(0, 12))

        self.right = Frame(self.content, bg='teal')
        self.right.pack(side='right', fill='both', expand=True, padx=(12, 0))

        # CTA + result card
        self.start_button()
        self._build_result_card()

    # ---------- UI pieces ----------
    def start_button(self):
        self.start_btn = Button(
            self.left, text="Start", command=self.show_searchbar,
            bg="#0ea5e9", fg="white", bd=0,
            font=("Helvetica", 14, "bold"),
            activebackground="#0284c7", activeforeground="white",
            relief="flat", padx=16, pady=10, cursor="hand2",
            highlightthickness=2, highlightbackground="teal",
            highlightcolor="#38bdf8"
        )
        self.start_btn.pack(pady=16, ipadx=4)
        self.start_btn.bind("<Enter>", lambda e: e.widget.configure(bg="#0284c7"))
        self.start_btn.bind("<Leave>", lambda e: e.widget.configure(bg="#0ea5e9"))

    def show_searchbar(self):
        if hasattr(self, "start_btn") and self.start_btn.winfo_exists():
            self.start_btn.destroy()

        self.search_group = Frame(self.left, bg="teal")
        self.search_group.pack(pady=8, fill="x")

        self.search_wrap = Frame(self.search_group, bg="#008080")
        self.search_wrap.pack(fill="x", padx=2, pady=2)

        self.search_var = StringVar()
        placeholder = "Enter ZIP or coordinates (lat, lon)"

        self.search_entry = Entry(
            self.search_wrap, textvariable=self.search_var,
            font=("Helvetica", 12), bg="#f0f8ff", fg="#95a5a6",
            relief="flat", insertbackground="#2c3e50",
            highlightthickness=1, highlightbackground="#008080",
            highlightcolor="#00a0a0"
        )
        self.search_entry.pack(side="left", fill="x", expand=True,
                               ipady=10, padx=(15, 5), pady=5)
        self.search_var.set(placeholder)

        def on_entry_click(_):
            if self.search_var.get() == placeholder:
                self.search_var.set("")
                self.search_entry.config(fg="#2c3e50")

        def on_focusout(_):
            if self.search_var.get().strip() == "":
                self.search_var.set(placeholder)
                self.search_entry.config(fg="#95a5a6")

        self.search_entry.bind("<FocusIn>", on_entry_click)
        self.search_entry.bind("<FocusOut>", on_focusout)
        self.search_entry.bind("<Return>", lambda _e: self._do_search())

        self.search_button = Button(
            self.search_wrap, text="🔍 Search",
            font=("Helvetica", 11, "bold"),
            bg="#00a0a0", fg="white",
            activebackground="#008080", activeforeground="white",
            relief="flat", bd=0, command=self._do_search
        )
        self.search_button.pack(side="right", padx=(5, 15),
                                pady=5, ipadx=15, ipady=8)
        self.search_button.bind("<Enter>", lambda e: e.widget.configure(bg="#008080"))
        self.search_button.bind("<Leave>", lambda e: e.widget.configure(bg="#00a0a0"))

        self.status = Label(self.left, text="", bg='teal', fg='#e0f2f1',
                            font=("Helvetica", 10))
        self.status.pack(anchor='w', pady=(6, 0))

    def _build_result_card(self):
        # Outer card
        self.card = Frame(self.right, bg="#0d9488")
        self.card.pack(fill="both", expand=True, pady=6)

        # Inner content surface
        self.card_inner = Frame(self.card, bg="#134e4a")
        self.card_inner.pack(fill="both", expand=True, padx=10, pady=10)

        # Location
        self.loc_label = Label(
            self.card_inner, text="Location —",
            font=("Helvetica", 18, "bold"),
            fg="#ecfeff", bg="#134e4a"
        )
        self.loc_label.pack(anchor="w", pady=(2, 6))

        # Temperature big
        self.temp_label = Label(
            self.card_inner, text="— °",
            font=("Helvetica", 44, "bold"),
            fg="#a7f3d0", bg="#134e4a"
        )
        self.temp_label.pack(anchor="w", pady=(2, 2))

        # Condition pill
        self.cond_wrap = Frame(self.card_inner, bg="#134e4a")
        self.cond_wrap.pack(anchor="w", pady=(0, 10))
        self.cond_pill = Label(
            self.cond_wrap, text="—",
            font=("Helvetica", 12, "bold"),
            fg="#064e3b", bg="#a7f3d0",
            padx=10, pady=4
        )
        self.cond_pill.pack(side="left")

    # ---------- Logic ----------
    def _do_search(self):
        query = self.search_var.get().strip() if hasattr(self, 'search_var') else ""
        if not query or "Enter ZIP" in query:
            self._set_status("Type a ZIP or coordinates first.")
            return

        try:
            _ = self.master.Get_Weather(query)  # updates self.master.forecast
            fc = getattr(self.master, "forecast", None)

            if isinstance(fc, dict):
                location = fc.get("location", "—")
                temp = fc.get("temp", "—")
                weather = fc.get("weather", "—")
            else:
                location, temp, weather = "—", "—", str(_)

            self._render_summary(location, temp, weather)
            self._set_status("Updated ✓")
        except Exception as e:
            self._render_summary("—", "—", "Error")
            self._set_status(f"Error: {e}")

    def _render_summary(self, location, temp, weather):
        self.loc_label.config(text=location)
        s = str(temp)
        if "°" not in s:
            s = f"{s}°"
        self.temp_label.config(text=s)
        pretty = (weather or "—").strip().title()
        self.cond_pill.config(text=pretty)

    def _set_status(self, msg):
        if hasattr(self, "status"):
            self.status.config(text=msg)


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
    
    def update_task_list(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        for task in self.master.task_manager.get_all_tasks():
            task_frame = Frame(self.task_list_frame, bg='teal')
            task_frame.pack(fill="x", pady=2)
            
            status = "✓" if task['completed'] else "○"
            color = "light gray" if task['completed'] else "white"
            task_text = f"{status} {task['description']} ({task['category']})"
            
            Label(task_frame, text=task_text, fg=color, bg='teal', 
                  font=("Arial", 11)).pack(side="left")
            
            if not task['completed']:
                Button(task_frame, text="Complete", 
                      command=lambda t=task: self.complete_task(t['id']),
                      font=("Arial", 8)).pack(side="right")
    
    def complete_task(self, task_id):
        self.master.task_manager.complete_task(task_id)
        self.update_task_list()

class Setting_Window(Toplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title('Settings')
        self.geometry('400x400')
        self.setting_label = Label(self, text='Settings', font=('Helvetica', 20)).pack(anchor='w', padx=10)

        self.Sliders("Master")
        self.Sliders("Music")
        self.Sliders("SFX")

    def Sliders(self, name):
        self.slider_label = Label(self, text=name).pack(anchor='w', padx=10)
        self.Slider = Scale(self, from_=0, to=100, orient="horizontal")
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
    # Convert current weather to SuggestionEngine format
    try:
        if hasattr(self.master, 'forecast') and isinstance(self.master.forecast, dict):
            return {
                'description': self.master.forecast.get('weather', '').lower(),
                'temperature': self.master.forecast.get('temp', 72),
                'conditions': self.master.forecast.get('weather', '').lower(),
                'location': self.master.forecast.get('location', 'Current Location')
            }
    except Exception:
        pass
    return None
