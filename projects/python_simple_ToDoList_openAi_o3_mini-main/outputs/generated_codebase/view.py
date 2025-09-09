import tkinter as tk
from tkinter import messagebox, simpledialog


class ToDoView:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo List Application")
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.task_entry = tk.Entry(self.frame, width=50)
        self.task_entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.add_button = tk.Button(self.frame, text="Add Task")
        self.add_button.grid(row=0, column=4, padx=5, pady=5)

        self.task_listbox = tk.Listbox(self.frame, width=70)
        self.task_listbox.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

        self.edit_button = tk.Button(self.frame, text="Edit Task")
        self.edit_button.grid(row=2, column=0, padx=5, pady=5)

        self.complete_button = tk.Button(self.frame, text="Mark Complete")
        self.complete_button.grid(row=2, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.frame, text="Delete Task")
        self.delete_button.grid(row=2, column=2, padx=5, pady=5)

        self.refresh_button = tk.Button(self.frame, text="Refresh")
        self.refresh_button.grid(row=2, column=3, padx=5, pady=5)

    def get_task_input(self):
        return self.task_entry.get()

    def clear_task_input(self):
        self.task_entry.delete(0, tk.END)

    def set_task_list(self, tasks):
        self.task_listbox.delete(0, tk.END)
        for index, task in enumerate(tasks):
            display_text = f"{index + 1}. {task['description']} - {task['status']}"
            self.task_listbox.insert(tk.END, display_text)

    def get_selected_task_index(self):
        try:
            index = self.task_listbox.curselection()[0]
            return index
        except IndexError:
            messagebox.showwarning("Select Task", "No task selected.")
            return None

    def prompt_task_edit(self, current_text):
        return simpledialog.askstring("Edit Task", "Edit task description:", initialvalue=current_text)

    def display_error(self, message):
        messagebox.showerror("Error", message)

    def display_info(self, message):
        messagebox.showinfo("Info", message)
