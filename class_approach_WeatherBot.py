from tkinter import *
import tkinter as tk


#class approach calls window by organizing data in a class...
class Weather_Main_Window(Tk):
    def __init__(self):
        super().__init__()
        
        #title, icon, size
        self.title('WeatherBot')
        self.geometry("800x600")
        self.configure(bg='teal')
       

        #label
        self.my_label = Label(self, text='Welcome to WeatherBot', font=('Helvetica', 42))
        self.my_label.pack(pady=20)
    
    def Weather_Button(self):
        self.weather_button = Button(text="Get Weather Info", command=lambda: Weather_Window(), bg="#333", fg="white", bd=0)
        self.weather_button.pack(pady=30)
        
    def Todo_Button(self):
        self.todo_button = Button(text='To Do list', command=Todo_Window, bg='#333',fg='white',bd=0)
        self.todo_button.pack(pady=70)
    
    def Setting_Button(self):
        self.img = PhotoImage(file="gear.png").subsample(3, 3)
        self.menu = Menu(self, tearoff=0, bg="red", fg="black")
        self.setting_button = Button(self, image=self.img, bd=0, relief="flat", highlightthickness=0,
                bg="teal", activebackground="teal", command=Setting_Window)
        self.setting_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
    
    def Exit_button(self):
        self.exit_button = Button(text='Exit',command=self.destroy, bg='#333',fg='white',bd=0)
        self.exit_button.pack(pady=75)

    


class Weather_Window(Tk):
   
    def __init__(self): 
        super().__init__()

        
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
        self.start_btn.destroy()  # Remove the start button
        
        # Create search variable
        self.search_var = tk.StringVar()
        
        # Create a stylish search frame with gradient effect
        search_frame = tk.Frame(self, bg="teal")
        search_frame.pack(pady=20, padx=30, fill="x")
        
        # Create a container for the search elements with a gradient-like effect
        inner_frame = tk.Frame(search_frame, bg="#008080")  # Darker teal
        inner_frame.pack(fill="x", padx=2, pady=2)
        
        # Search entry with modern styling
        search_entry = tk.Entry(inner_frame, textvariable=self.search_var, 
                           font=("Segoe UI", 12), bg="#f0f8ff", fg="#2c3e50",
                           relief="flat", insertbackground="#2c3e50")
        
        # Add placeholder text
        def on_entry_click(event):
            if self.search_var.get() == "Enter location or activity...":
                self.search_var.set("")
                search_entry.config(fg="#2c3e50")
        
        def on_focusout(event):
            if self.search_var.get() == "":
                self.search_var.set("Enter location or activity...")
                search_entry.config(fg="#95a5a6")
        
        self.search_var.set("Enter location or activity...")
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
                              command=lambda: print("Search clicked"))
        
        def on_hover_enter(e):
            search_button.config(bg="#008080")
        
        def on_hover_leave(e):
            search_button.config(bg="#00a0a0")
        
        search_button.bind("<Enter>", on_hover_enter)
        search_button.bind("<Leave>", on_hover_leave)
        
        # Pack the search button with proper padding
        search_button.pack(side="right", padx=(5, 15), pady=5, ipadx=15, ipady=8)
    
    
class Todo_Window(Tk):
    
    def __init__(self): 
        
        super().__init__()

        
         #title, icon, size
        self.title('To Do list')
        self.geometry("800x600")
        self.configure(bg='teal')
        self.tasks =[]

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
            self.listbox.insert(tk.END, self.task)
            self.entry_box.delete(0, tk.END)  # clear the entry field


class Setting_Window(Tk):
    
    def __init__(self):
        super().__init__()
     
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

       
#instantiation
app = Weather_Main_Window()





app.Weather_Button()


app.Todo_Button()

app.Setting_Button()
app.Exit_button()





      
app.mainloop()













