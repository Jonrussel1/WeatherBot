from tkinter import END, Button, Entry, Frame, Label, Radiobutton, StringVar, Toplevel


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