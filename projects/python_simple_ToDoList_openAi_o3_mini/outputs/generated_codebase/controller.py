import logging
from model import Task, TaskManager
from persistence import FileManager
from view import ToDoView


class ToDoController:
    def __init__(self, root):
        self.root = root
        self.task_manager = TaskManager()
        self.file_manager = FileManager()
        self.view = ToDoView(root)
        self.setup_callbacks()
        self.load_tasks()

    def setup_callbacks(self):
        self.view.add_button.config(command=self.add_task)
        self.view.edit_button.config(command=self.edit_task)
        self.view.complete_button.config(command=self.complete_task)
        self.view.delete_button.config(command=self.delete_task)
        self.view.refresh_button.config(command=self.refresh_view)

    def load_tasks(self):
        data = self.file_manager.load_data()
        self.task_manager.load_from_list(data)
        self.refresh_view()

    def add_task(self):
        description = self.view.get_task_input().strip()
        if not description:
            self.view.display_error("Task description cannot be empty.")
            return
        new_task = Task(description=description)
        self.task_manager.add_task(new_task)
        self.save_tasks()
        self.refresh_view()
        self.view.clear_task_input()

    def edit_task(self):
        index = self.view.get_selected_task_index()
        if index is None:
            return
        tasks = self.task_manager.get_tasks()
        current_task = tasks[index]
        new_description = self.view.prompt_task_edit(current_task.description)
        if new_description and new_description.strip():
            current_task.update(description=new_description.strip())
            self.task_manager.update_task(index, current_task)
            self.save_tasks()
            self.refresh_view()
        else:
            self.view.display_error("Invalid input for task edit.")

    def complete_task(self):
        index = self.view.get_selected_task_index()
        if index is None:
            return
        tasks = self.task_manager.get_tasks()
        task = tasks[index]
        task.mark_complete()
        self.task_manager.update_task(index, task)
        self.save_tasks()
        self.refresh_view()

    def delete_task(self):
        index = self.view.get_selected_task_index()
        if index is None:
            return
        self.task_manager.delete_task(index)
        self.save_tasks()
        self.refresh_view()

    def refresh_view(self):
        tasks_list = self.task_manager.to_list()
        self.view.set_task_list(tasks_list)

    def save_tasks(self):
        data = self.task_manager.to_list()
        self.file_manager.save_data(data)
