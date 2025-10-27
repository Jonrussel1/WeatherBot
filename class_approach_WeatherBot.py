from tkinter import *


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
        self.weather_button = Button(text="Get Weather Info", command=Weather_Window, bg="#333", fg="white", bd=0)
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
        self.start_btn.destroy()  # or: start_btn.pack_forget()
        self.topbar = Frame(self, bg="teal")
        self.topbar.pack(side="top", fill="x")
        q = StringVar()
        Entry(self.topbar, textvariable=q, font=("TkDefaultFont",12)).pack(side="left", padx=8, pady=8, fill="x", expand=True)
        Button(self.topbar, text="Search", bg="#333", fg="white", bd=0,
              command=lambda: q.set(f"Searching: {q.get()}")).pack(side="left", padx=6)
    
    
class Todo_Window(Tk):
    
    def __init__(self): 
        
        super().__init__()

        
         #title, icon, size
        self.title('To Do list')
        self.geometry("800x600")
        self.configure(bg='teal')


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