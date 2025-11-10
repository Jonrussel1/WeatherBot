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
        self.forecast = "No Forecast"
       

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
        self.todo_button = Button(self, text='To Do list', command=self.Open_ToDo_Window, bg='#333', fg='white', bd=0)
        self.todo_button.pack(pady=16)
        # secondary neutral button
        self.todo_button.configure(
            font=("Helvetica", 14, "bold"),
            bg="#1f2937", fg="white",
            activebackground="#374151", activeforeground="white",
            bd=0, relief="flat", padx=16, pady=10, cursor="hand2",
            highlightthickness=2, highlightbackground=self["bg"], highlightcolor="#0284c7"
        )
        self.todo_button.bind("<Enter>", lambda e: e.widget.configure(bg="#374151"))
        self.todo_button.bind("<Leave>", lambda e: e.widget.configure(bg="#1f2937"))

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
        # fixed quoting so the f-string is valid
        self.forecast = self.weather.get_weather(coords)
        return f'Current Weather: {self.forecast["weather"].title()} | Temperature: {self.forecast["temp"]} | Location: {self.forecast["location"]}'

    def Suggestion_button(self):
        self.suggest_button = Button(self, text='Recommend', command=self.Open_Suggestion_Window, bg='#333', fg='white', bd=0)
        self.suggest_button.pack(pady=16)
        self.suggest_button.configure(
            font=("Helvetica", 14, "bold"),
            bg="#0ea5e9", fg="white",
            activebackground="#0284c7", activeforeground="white",
            bd=0, relief="flat", padx=14, pady=8, cursor="hand2",
            highlightthickness=2, highlightbackground=self["bg"], highlightcolor="#0284c7"
        )

        self.suggest_button.bind("<Enter>", lambda e: e.widget.configure(bg="#0284c7"))
        self.suggest_button.bind("<Leave>", lambda e: e.widget.configure(bg="teal"))

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

        # title, icon, size
        self.title('To Do list')
        self.geometry("800x600")
        self.configure(bg='teal')
        self.tasks = []

        self.entry_box = Entry(self, width=40, font=("Arial", 14))
        self.entry_box.pack(pady=20)

        self.button = Button(self, text="Add Task", command=self.add_task)
        self.button.pack()

        self.listbox = Listbox(self, width=50, height=10, font=("Arial", 14))
        self.listbox.pack(pady=10)

    def add_task(self):
        self.task = self.entry_box.get()
        if self.task:
            # Add the task to the list
            self.tasks.append(self.task)
            self.listbox.insert("end", self.task)
            self.entry_box.delete(0, "end")  # clear the entry field


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
        # title, icon, size
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













