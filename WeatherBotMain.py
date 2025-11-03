import tkinter as tk
import Weather
import os
from SuggestionEngine import SuggestionEngine

# to get the location of the current python file
basedir = os.path.dirname(os.path.abspath(__file__))

# Initialize suggestion engine
suggestion_engine = SuggestionEngine()

root = tk.Tk(className= "Weather Bot");  root.geometry("800x600"); root.configure(bg="teal") #SETS UP WINDOW
msg = tk.StringVar(value="Weather Bot") #VARIABLE TO HOLD TEXT
tk.Label(root, textvariable=msg, font=("TkDefaultFont",16), fg="Orange", bg="teal").pack(pady=10) #DISPLAYS TEXT

# Global variable to store current coordinates
current_coords = "32.9004,-105.9629"
 
#DEFINES SETTINGS WINDOW
 
def open_settings():
    w = tk.Toplevel(root); w.title("Settings"); w.resizable(False, False)
    def add_slider(name, val=70):
        tk.Label(w, text=name).pack(anchor="w", padx=10)
        # SLIDER
        s = tk.Scale(w, from_=0, to=100, orient="horizontal"); s.set(val); s.pack(padx=10, pady=2, fill="x")
        return s
    # SLIDERS
    master = add_slider("Master")
    music  = add_slider("Music")
    sfx    = add_slider("SFX")
search_var = tk.StringVar()

def open_task_manager():
    # Open a window to manage tasks
    task_window = tk.Toplevel(root)
    task_window.title("Task Manager")
    task_window.geometry("400x300")

    # Task input frame
    input_frame = tk.Frame(task_window)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Task:").pack(side="left")
    task_entry = tk.Entry(input_frame, width=20)
    task_entry.pack(side="left", padx=5)

    category_var = tk.StringVar(value="outdoor")
    tk.Radiobutton(input_frame, text="Outdoor", variable=category_var, value="outdoor").pack(side="left")
    tk.Radiobutton(input_frame, text="Indoor", variable=category_var, value="indoor").pack(side="left")
    
    def add_new_task():
        description = task_entry.get().strip()
        if description:
            suggestion_engine.add_task(description, category_var.get())
            task_entry.delete(0, tk.END)
            update_suggestions_display()
            update_task_list()
    
    tk.Button(input_frame, text="Add Task", command=add_new_task).pack(side="left", padx=5)

    # Task list frame
    list_frame = tk.Frame(task_window)
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.label(list_frame, text="Your Tasks:", font=("TkDefaultFont", 12, "bold")).pack(anchor="w")

    task_list_frame = tk.Frame(list_frame)
    task_list_frame.pack(fill="both", expand=True)

    def update_task_list():
        # Clear existing task list
        for widget in task_list_frame.winfo_children():
            widget.destroy()

        # Add current tasks
        for task in suggestion_engine.get_all_tasks:
            task_frame = tk.Frame(task_list_frame)
            task_frame.pack(fill="x", pady=2)

            status = "DONE" if task['completed'] else "IN PROGRESS"
            color = "green" if task['completed'] else "red"
            task_text = f"{status}{task['description']} ({task['category']})"

            tk.Label(task_frame, text=task_text, fg=color).pack(side="left")

            if not task['completed']:
                tk.button(task_frame, text="Complete", command=lambda t=task: complete_task(t['id']), font=("TkDefaultFont", 8)).pack(side="right")

    def complete_task(task_id):
        suggestion_engine.complete_task(task_id)
        update_task_list()
        update_suggestions_display()   

    update_task_list()

search_var = tk.StringVar()
suggestions_var = tk.StringVar(value="Suggestions will appear here...")           
        
 
# DEFINES SEARCH BAR
def show_searchbar():
    start_btn.destroy()  # or: start_btn.pack_forget()
    
    # Instructions label
    instructions = tk.Label(root, text="Enter coordinates as latitude,longitude\nExample: 32.9004,-105.9629", bg="teal", fg="white",
font=("TkDefaultFont", 10))
    instructions.pack(pady=5)

    # Create a stylish search frame with gradient effect
    search_frame = tk.Frame(root, bg="teal")
    search_frame.pack(pady=20, padx=30, fill="x")
    
    # Create a container for the search elements with a gradient-like effect
    inner_frame = tk.Frame(search_frame, bg="#008080")  # Darker teal
    inner_frame.pack(fill="x", padx=2, pady=2)
    
    # Search entry with modern styling
    search_entry = tk.Entry(inner_frame, textvariable=search_var, 
                           font=("Segoe UI", 12), bg="#f0f8ff", fg="#2c3e50",
                           relief="flat", insertbackground="#2c3e50")
    
    # Add placeholder text
    def on_entry_click(event):
        if search_var.get() == "e.g., 32.9004,-105.9629":
            search_var.set("")
            search_entry.config(fg="#2c3e50")
    
    def on_focusout(event):
        if search_var.get() == "":
            search_var.set("Enter location or activity...")
            search_entry.config(fg="#95a5a6")
    
    search_var.set("Enter location or activity...")
    search_entry.config(fg="#95a5a6")
    search_entry.bind('<FocusIn>', on_entry_click)
    search_entry.bind('<FocusOut>', on_focusout)
    
    # Style the entry
    search_entry.config(highlightthickness=1, highlightbackground="#008080", highlightcolor="#00a0a0")
    search_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(15, 5), pady=5)
    
    # Create a simple search button (hover changes color)
    search_button = tk.Button(inner_frame, text="🔍 Search", font=("Segoe UI", 11, "bold"),
                              bg="#00a0a0", fg="white", activebackground="#008080",
                              activeforeground="white", relief="flat", bd=0,
                              command=lambda:update_weather())

    def on_hover_enter(e):
        search_button.config(bg="#008080")

    def on_hover_leave(e):
        search_button.config(bg="#00a0a0")

    search_button.bind("<Enter>", on_hover_enter)
    search_button.bind("<Leave>", on_hover_leave)

    # Pack the search button with proper padding
    search_button.pack(side="right", padx=(5, 15), pady=5, ipadx=15, ipady=8)

    task_button = tk.button(root, text="Manage Tasks", font=("Segoe UI", 12), bg="00a0a0", fg="white", 
                            command=open_task_manager)
    task_button.pack(pady=10)

start_btn = tk.Button(root, text="Start", command=show_searchbar, bg="#333", fg="white", bd=0); start_btn.pack()
 
 
# CREATES SETTINGS MENU
menu = tk.Menu(root, tearoff=0, bg="red", fg="black")
 
 
# CALLS SETTINGS WINDOW
menu.add_command(label="Settings", command=open_settings)
 
# Calls Task Manager
menu.add_command(label="Task Manager", command=open_task_manager)

# ADDS EXIT OPTION
menu.add_separator(); menu.add_command(label="Exit", command=root.destroy)
 
#combine basedir with gear.png to access it
gear_img_location = os.path.join(basedir,'gear.png')
 
# SETTINGS BUTTON
img = tk.PhotoImage(file=gear_img_location).subsample(3, 3)
btn = tk.Button(root, image=img, bd=0, relief="flat", highlightthickness=0,
                bg="teal", activebackground="teal",
                command=lambda: menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery()))  #open menu
btn.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
 
forecast_var = tk.StringVar(value="Weather data will appear here")
#displays whatever is in forecast_var
forecast_label = tk.Label(root, textvariable=forecast_var, bg="teal", fg="white", font=("TkDefaultFont", 12))
forecast_label.place(anchor="center", relx = 0.5, rely = 0.25)

#Suggestions display
suggestions_label = tk.Label(root, textvariable=suggestions_var, justify="left", font=("TkDefaultFont", 10), bg="teal", fg="white")
suggestions_label.place(anchor="center", relx = 0.5, rely = 0.6)

def update_suggestions_display():
    #Update the suggestions display based on current weather
    try:
        weather_obj = Weather.Get_Weather()
        raw_data = weather_obj.get_weather_simple(*current_coords.split(','))
        suggestions = suggestion_engine.generate_suggestions(raw_data)
        suggestions_text = "Today's Suggestions:\n" + "\n".join(suggestions)
        suggestions_var.set(suggestions_text)
    except Exception as e:
        suggestions_var.set("Suggestions:\nEnter valid coordinates to see suggestions")

def update_weather():
    global current_coords
    coords_input = search_var.get().strip()
    
    # Handle the placeholder text
    if coords_input == "e.g., 32.9004,-105.6929":
        forecast_var.set("Please enter valid coordinates.")
        return 
    
    try:
        # Basic coordinate validation
        if ',' not in coords_input:
            forecast_var.set("Error: Use Format: latitude,longitude")
            return
        lat, lon = coords_input.split(',', 1)
        lat = lat.strip()
        lon = lon.strip()

        # Simple validation
        float(lat)
        float(lon)

        current_coords = f"{lat},{lon}"

        # Get weather data
        weather_obj = Weather.Get_Weather()
        weather_text = weather_obj.get_weather(current_coords)
        forecast_var.set(weather_text)

        # Update suggestions
        update_suggestions_display()

    except ValueError:
        forecast_var.set("Error: Coordinates must be numbers\nExample: 32.9004,-105.9629")
    except Exception as e:
        forecast_var.set(f"Error getting weather data: {str(e)}")     

# Add some sample tasks for demonstration
suggestion_engine.add_task("Mow the lawn", "outdoor")
suggestion_engine.add_task("Wash the car", "outdoor")
suggestion_engine.add_task("Clean the garage", "indoor")
suggestion_engine.add_task("Organize the pantry", "indoor")

# Initialize with default location
update_weather()
 
root.mainloop() #RUNS PROGRAM
 


