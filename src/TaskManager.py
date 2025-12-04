import json
import os

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.data_file = "tasks.json"
        self.load_tasks()
    
    def add_task(self, description, category="outdoor"):
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "category": category.lower(),
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
    
    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                break
        self.save_tasks()
    
    def get_tasks_by_category(self, category):
        return [task for task in self.tasks if task["category"] == category.lower() and not task["completed"]]
    
    def get_incomplete_tasks(self):
        return [task for task in self.tasks if not task["completed"]]
    
    def get_all_tasks(self):
        return self.tasks
    
    def save_tasks(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f)
        except:
            print("Could not save tasks")
    
    def load_tasks(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
        except:
            print("Could not load tasks")
            self.tasks = []