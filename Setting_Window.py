from tkinter import Label, Scale, Toplevel


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