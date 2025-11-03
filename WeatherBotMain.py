import tkinter as tk
from tkinter import ttk, messagebox
import os
import weatherapi as weather_api
from task_manager import TaskManager
from suggestion_engine import SuggestionEngine

# to get the location of the current python file
basedir = os.path.dirname(os.path.abspath(__file__))

class WeatherBot:
    def __init__(self, root):
        self.root = root
        self.root.title("WeatherBot - Weather Planner")
        self.root.geometry("800x600")
        self.root.configure(bg="teal")
        
        # Initialize modules
        self.weather_api = weather_api.WeatherAPI()
        self.task_manager = TaskManager()
        self.suggestion_engine = SuggestionEngine()
        
        # Global variable to store current coordinates
        self.current_coords = "32.9008,105.9602"  # Default coordinates (Alamogordo, NM)
        
        # Setup UI using coordinates-only interface
        self.setup_ui()
        
        # Add sample tasks for demonstration
        self._add_sample_tasks()
        
        # Initialize with default location
        self.forecast_var.set("Enter coordinates below to get weather")
        self.suggestions_var.set("Add tasks and get weather for personalized suggestions!")
    
    def setup_ui(self):
        # Setup UI
        msg = tk.StringVar(value="WeatherBot")
        tk.Label(self.root, textvariable=msg, font=("TkDefaultFont",16), fg="Orange", bg="teal").pack(pady=10)
        
        # Your existing search bar setup - modified for coordinates only
        self.search_var = tk.StringVar()
        self.forecast_var = tk.StringVar(value="Enter coordinates above to get weather")
        self.suggestions_var = tk.StringVar(value="Add tasks and get weather for personalized suggestions!")
        
        self._create_coordinate_input()
        self._create_weather_display()
        self._create_suggestions_display()
        self._create_task_manager_button()
        self._create_settings_menu()
    
    def _create_coordinate_input(self):
        # Coordinate input section
        # Detailed instructions
        instructions = tk.Label(self.root, 
            text="Format: latitude,longitude\nExamples:\n40.7128,-74.0060 (New York)\n34.0522,-118.2437 (Los Angeles)", 
            bg="teal", fg="white", font=("TkDefaultFont", 9), justify="left")
        instructions.pack(pady=5)
        
        # Coordinate input frame
        input_frame = tk.Frame(self.root, bg="teal")
        input_frame.pack(pady=15, padx=30, fill="x")
        
        inner_frame = tk.Frame(input_frame, bg="#008080")
        inner_frame.pack(fill="x", padx=2, pady=2)
        
        # Coordinate entry with better placeholder
        coord_entry = tk.Entry(inner_frame, textvariable=self.search_var, 
                               font=("Segoe UI", 12), bg="#f0f8ff", fg="#2c3e50",
                               relief="flat", insertbackground="#2c3e50")
        
        def on_entry_click(event):
            if self.search_var.get() == "e.g., 32.9008,105.9602":
                self.search_var.set("")
                coord_entry.config(fg="#2c3e50")
        
        def on_focusout(event):
            if self.search_var.get() == "":
                self.search_var.set("e.g., 32.9008,105.9602")
                coord_entry.config(fg="#95a5a6")
        
        self.search_var.set("e.g., 32.9008,105.9602")
        coord_entry.config(fg="#95a5a6")
        coord_entry.bind('<FocusIn>', on_entry_click)
        coord_entry.bind('<FocusOut>', on_focusout)
        
        coord_entry.config(highlightthickness=1, highlightbackground="#008080", highlightcolor="#00a0a0")
        coord_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(15, 5), pady=5)
        
        # Search button
        search_button = tk.Button(inner_frame, text="🔍 Get Weather", font=("Segoe UI", 11, "bold"),
                                  bg="#00a0a0", fg="white", activebackground="#008080",
                                  activeforeground="white", relief="flat", bd=0,
                                  command=self.update_weather)

        def on_hover_enter(e):
            search_button.config(bg="#008080")

        def on_hover_leave(e):
            search_button.config(bg="#00a0a0")

        search_button.bind("<Enter>", on_hover_enter)
        search_button.bind("<Leave>", on_hover_leave)
        search_button.pack(side="right", padx=(5, 15), pady=5, ipadx=15, ipady=8)
        
        # Quick coordinate examples
        example_frame = tk.Frame(self.root, bg="teal")
        example_frame.pack(pady=5)
        
        tk.Label(example_frame, text="Try:", bg="teal", fg="white").pack(side="left")
        
        # Example buttons
        examples = [
            ("NYC", "40.7128,-74.0060"),
            ("LA", "34.0522,-118.2437"), 
            ("London", "51.5074,-0.1278"),
            ("Tokyo", "35.6762,139.6503")
        ]
        
        for name, coords in examples:
            btn = tk.Button(example_frame, text=name, font=("TkDefaultFont", 8),
                           bg="#34495e", fg="white", relief="flat",
                           command=lambda c=coords: self.load_example_coords(c))
            btn.pack(side="left", padx=2)
    
    def load_example_coords(self, coords):
        # Load example coordinates
        self.search_var.set(coords)
        self.update_weather()
    
    def _create_weather_display(self):
        # Weather display area
        self.forecast_label = tk.Label(self.root, textvariable=self.forecast_var, 
                                      bg="teal", fg="white", font=("TkDefaultFont", 11),
                                      justify="center")
        self.forecast_label.place(anchor="center", relx=0.5, rely=0.22)
    
    def _create_suggestions_display(self):
        # Suggestions display area
        self.suggestions_label = tk.Label(self.root, textvariable=self.suggestions_var, justify="left", 
                                        font=("TkDefaultFont", 10), bg="teal", fg="white", 
                                        wraplength=600)
        self.suggestions_label.place(anchor="center", relx=0.5, rely=0.7)
    
    def _create_task_manager_button(self):
        # Button to open task manager
        self.task_button = tk.Button(self.root, text="📋 Manage Tasks", font=("Segoe UI", 11),
                                   bg="#00a0a0", fg="white", command=self.open_task_manager)
        self.task_button.pack(pady=10)
    
    def _create_settings_menu(self):
        # Setting Menu
        menu = tk.Menu(self.root, tearoff=0, bg="red", fg="black")
        menu.add_command(label="Settings", command=self.open_settings)
        menu.add_command(label="Manage Tasks", command=self.open_task_manager)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.root.destroy)
        
        gear_img_location = os.path.join(basedir, 'gear.png')
        
        try:
            img = tk.PhotoImage(file=gear_img_location).subsample(3, 3)
            btn = tk.Button(self.root, image=img, bd=0, relief="flat", highlightthickness=0,
                            bg="teal", activebackground="teal",
                            command=lambda: menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery()))
            btn.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        except:
            btn = tk.Button(self.root, text="⚙", font=("TkDefaultFont", 12), bd=0,
                            bg="teal", activebackground="teal",
                            command=lambda: menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery()))
            btn.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
    
    def open_task_manager(self):
        # Open task manager window
        task_window = tk.Toplevel(self.root)
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
                self.task_manager.add_task(description, category_var.get())
                task_entry.delete(0, tk.END)
                self.update_suggestions_display()
                self.update_task_list()
        
        tk.Button(input_frame, text="Add Task", command=add_new_task).pack(side="left", padx=5)
        
        # Task list frame
        list_frame = tk.Frame(task_window)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(list_frame, text="Your Tasks:", font=("TkDefaultFont", 12, "bold")).pack(anchor="w")
        
        self.task_list_frame = tk.Frame(list_frame)
        self.task_list_frame.pack(fill="both", expand=True)
        
        self.update_task_list()
    
    def update_task_list(self):
        # Update the task list display
        if hasattr(self, 'task_list_frame'):
            for widget in self.task_list_frame.winfo_children():
                widget.destroy()
            
            for task in self.task_manager.get_all_tasks():
                task_frame = tk.Frame(self.task_list_frame)
                task_frame.pack(fill="x", pady=2)
                
                status = "✓" if task['completed'] else "○"
                color = "gray" if task['completed'] else "black"
                task_text = f"{status} {task['description']} ({task['category']})"
                
                tk.Label(task_frame, text=task_text, fg=color).pack(side="left")
                
                if not task['completed']:
                    tk.Button(task_frame, text="Complete", 
                             command=lambda t=task: self.complete_task(t['id']),
                             font=("TkDefaultFont", 8)).pack(side="right")
    
    def complete_task(self, task_id):
        # Complete a task and update suggestions
        self.task_manager.complete_task(task_id)
        self.update_task_list()
        self.update_suggestions_display()
    
    def open_settings(self):
        # Settings window
        w = tk.Toplevel(self.root)
        w.title("Settings")
        w.resizable(False, False)
        
        def add_slider(name, val=70):
            tk.Label(w, text=name).pack(anchor="w", padx=10)
            s = tk.Scale(w, from_=0, to=100, orient="horizontal")
            s.set(val)
            s.pack(padx=10, pady=2, fill="x")
            return s
        
        master = add_slider("Master")
        music = add_slider("Music")
        sfx = add_slider("SFX")
    
    def update_weather(self):
        # Update weather based on coordinate input
        coords_input = self.search_var.get().strip()
        
        if coords_input == "e.g., 32.9008,105.9602":
            self.forecast_var.set("Please enter valid coordinates below")
            return
        if coords_input == "e.g., 32.9008,105.9602":
            messagebox.showwarning("Input Needed", "Please enter coordinates in the format: latitude,longitude")
            return
        
        try:
            if ',' not in coords_input:
                messagebox.showerror("Format Error", "Please use format: latitude,longitude\nExample: 32.9008,105.9602")
                return
                
            lat, lon = coords_input.split(',', 1)
            lat = lat.strip()
            lon = lon.strip()
            
            # Basic validation
            lat_num = float(lat)
            lon_num = float(lon)
            
            if not (-90 <= lat_num <= 90):
                messagebox.showerror("Invalid Coordinates", "Latitude must be between -90 and 90")
                return
            if not (-180 <= lon_num <= 180):
                messagebox.showerror("Invalid Coordinates", "Longitude must be between -180 and 180")
                return
            
            self.current_coords = f"{lat},{lon}"
            
            # Get weather data using the coordinate-only approach
            print(f"Calling get_weather with: {self.current_coords}")
            weather_text = weather_api.get_weather(self.current_coords)
            print(f"Received: {weather_text}")
            
            # Update the display
            self.forecast_var.set(weather_text)

            # Update suggestions
            self.update_suggestions_display()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Coordinates must be numbers\nExample: 32.9008,105.9602")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to get weather data: {str(e)}")
    
    def update_suggestions_display(self):
        # Update suggestions based on current weather and tasks
        try:
            print(f"Updating suggestions for: {self.current_coords}")

            # Get REAL weather data for suggestions using coordinates
            weather_data = self.weather_api.get_weather_by_coords(*self.current_coords.split(','))
            
            # Check for errors in weather data
            if 'error' in weather_data:
                self.suggestions_var.set(f"Error: {weather_data['error']}")
                return
            
            print(f"Weather data for suggestions: {weather_data['description']} at {weather_data['temperature']}°F")

            # Generate suggestions using the REAL data
            suggestions = self.suggestion_engine.generate_suggestions(weather_data, self.task_manager)
            suggestions_text = "Smart Suggestions:\n" + "\n".join(suggestions)
            self.suggestions_var.set(suggestions_text)

            print(f"Suggestions generated: {len(suggestions)} items")         

        except Exception as e:
            error_msg = f"Error generating suggestions: {str(e)}"
            self.suggestions_var.set(error_msg)
            print(f"Suggestion error: {e}")
    
    def _add_sample_tasks(self):
        # Add some sample tasks for demonstration
        self.task_manager.add_task("Mow the lawn", "outdoor") 
        self.task_manager.add_task("Clean the garage", "indoor")

def main():
    root = tk.Tk()
    app = WeatherBot(root)
    root.mainloop()

if __name__ == "__main__":
    main()
 



