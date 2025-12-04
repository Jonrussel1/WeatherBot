from tkinter import Label, Scale, Toplevel


class Setting_Window(Toplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title('Settings')
        self.an = self.winfo_screenwidth()
        self.al = self.winfo_screenheight()
        self.tam = '%dx%d'%(self.an,self.al)
        self.geometry(self.tam)
        self.setting_label = Label(self, text='Settings', font=('Helvetica', 48), bg="#a7c7e7").pack(anchor='center',pady=60)
        
        self.Sliders("Master")
        self.Sliders("Music")
        self.Sliders("SFX")

    def Sliders(self, name):
        self.slider_label = Label(self, text=name,font=('Helvetica', 46),bg="#a7c7e7").pack(anchor="nw")
        self.Slider = Scale(self, from_=0, to=100, orient="horizontal")
        self.Slider.set(value=10)
        self.Slider.configure(font=("Helvetica", 34, "bold"))
        self.Slider.pack(padx=10, pady=2, fill="x")