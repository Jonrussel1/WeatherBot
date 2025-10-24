import tkinter as tk
import Weather
import os

# to get the location of the current python file
basedir = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk();  root.geometry("800x600"); root.configure(bg="teal") #SETS UP WINDOW
msg = tk.StringVar(value="WeatherBot") #VARIABLE TO HOLD TEXT
tk.Label(root, textvariable=msg, font=("TkDefaultFont",16), fg="Orange", bg="teal").pack(pady=10) #DISPLAYS TEXT

# ...existing code...
 
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
 
# DEFINES SEARCH BAR
def show_searchbar():
    start_btn.destroy()  # or: start_btn.pack_forget()
    topbar = tk.Frame(root, bg="teal"); topbar.pack(side="top", fill="x")
    q = tk.StringVar()
    tk.Entry(topbar, textvariable=q, font=("TkDefaultFont",12)).pack(side="left", padx=8, pady=8, fill="x", expand=True)
    tk.Button(topbar, text="Search", bg="#333", fg="white", bd=0,
              command=lambda: msg.set(f"Searching: {q.get()}")).pack(side="left", padx=6)
    #Once Search is pressed below will show weather info 

start_btn = tk.Button(root, text="Start", command=show_searchbar, bg="#333", fg="white", bd=0); start_btn.pack(),
 
 
# CREATES SETTINGS MENU
menu = tk.Menu(root, tearoff=0, bg="red", fg="black")
 
 
# CALLS SETTINGS WINDOW
menu.add_command(label="Settings", command=open_settings)
 
 
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
 
 
coords_var = tk.StringVar()
forecast_var = tk.StringVar(value="Current Weather: ")
forecast= ""


#displays whatver is in forecast_var
forecast_label = tk.Label(root, textvariable=forecast_var, text = forecast_var.get())

#whatevery is typed in is saved to coords_var
coords_entry = tk.Entry(root, textvariable = coords_var)

#gets coordinates from coords_var and runs get_weather with them, with error validation, then set forecast_var to weather or error message
def update_weather():
    coords = coords_var.get().split(',')
    coords_var.set("")
    try:
        forecast_var.set("Current Weather: " + Weather.get_weather(coords).title())
    except:
        forecast_var.set("Invalid Coordinates")

#button that runs update_weater() when clicked
submit_coords_btn = tk.Button(root, text = "Submit", command = update_weather)
forecast_label.place(relx=0.5, rely=0.2)
coords_entry.place(relx=0.5, rely=0.4)
submit_coords_btn.place(relx=0.5, rely=0.5)

 
root.mainloop() #RUNS PROGRAM
 

