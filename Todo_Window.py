from tkinter import END, Button, Entry, Frame, Label, Radiobutton, StringVar, Toplevel


class Todo_Window(Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        #title, icon, size
        self.title('Task Manager')
        self.geometry("2500x1450")
        self.configure(background="#678bb0")

        #Task input frame includes radio and task buttons
        self.input_frame = Frame(self, bg="#c6d9ed")
        self.input_frame.pack(side='top', pady=30, anchor='nw',fill='x')
        self.task_label = Label(self.input_frame, text='Tasks:', bg="#c6d9ed", fg="#1f2b33", font=("Helvetica",50))
        self.task_label.pack(pady=30, padx=5,side='left')
        self.task_entry = Entry(self.input_frame, font=('Helvetica',44))
        self.task_entry.pack(side='left',pady=30,padx=20)
        #radio buttons
        self.category_var = StringVar(value="outdoor")
        self.outdoor_b = Radiobutton(self.input_frame, text="Outdoor", variable=self.category_var, value="outdoor",
        bg="#c6d9ed", fg="#1f2b33",font=('Helvetica', 40))
        self.outdoor_b.pack(pady=30, side='left', padx=10)
        self.indoor_b = Radiobutton(self.input_frame, text="Indoor", variable=self.category_var, value="indoor",
        bg="#c6d9ed", fg="#1f2b33", font=('Helvetica', 40),borderwidth=10)
        self.indoor_b.pack(pady=30,side='left',padx=20)
        #add task button
        self.task_button = Button(self.input_frame, text="Add Task",bd=25, command=self.add_new_task,
        font=('Helvetica', 40))
        self.task_button.pack(side='right',pady=20,padx=10)
        
        #Task list frame includes tasks that were entered...
        self.list_frame = Frame(self, bg="#c6d9ed")
        self.list_frame.pack(fill="both",expand=True,anchor='n')
        
        self.your_tasks = Label(self.list_frame, text="Your Tasks:", font=("Helvetica", 46, "bold"), bg="#c6d9ed",fg="#1f2b33")
        self.your_tasks.pack(anchor="sw", pady=35)
        
        self.task_list_frame = Frame(self.list_frame, bg="#e8ebee")
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
            task_frame = Frame(self.task_list_frame, bg="#699cd3")
            task_frame.pack(fill="x", pady=20)

            status = "✓" if task['completed'] else "○"
            color = "#1f2b33" if task['completed'] else "red"
            task_text = f"{status} {task['description']} ({task['category']})"

            Label(task_frame, text=task_text, fg=color, bg="#c6d9ed",
            font=("Helvetica", 46)).pack(side="left")

            if not task['completed']:
                Button(task_frame, text="Complete",
                      command=lambda t=task: self.complete_task(t['id']),
                      font=("Helvetica", 46)).pack(side="bottom")

    def complete_task(self, task_id):
        self.master.task_manager.complete_task(task_id)
        self.update_task_list()