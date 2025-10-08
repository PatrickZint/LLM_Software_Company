import tkinter as tk
from tkinter import messagebox
import datetime

from db import NoteDatabase

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taking App")

        # Initialize the database
        self.db = NoteDatabase()

        # Set up the UI
        self.create_widgets()
        self.populate_notes()

    def create_widgets(self):
        # Frames for layout
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # List box to display notes
        self.note_list = tk.Listbox(self.left_frame, width=40)
        self.note_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.note_list.bind("<<ListboxSelect>>", self.on_note_select)

        # Note details on the right
        tk.Label(self.right_frame, text="Title:").pack(anchor="w")
        self.title_entry = tk.Entry(self.right_frame, width=50)
        self.title_entry.pack(fill=tk.X, pady=(0, 10))

        tk.Label(self.right_frame, text="Content:").pack(anchor="w")
        self.content_text = tk.Text(self.right_frame, width=50, height=15)
        self.content_text.pack(fill=tk.BOTH, pady=(0, 10))

        # Buttons for add, update, delete, clear
        self.button_frame = tk.Frame(self.right_frame)
        self.button_frame.pack()

        self.add_button = tk.Button(self.button_frame, text="Add", command=self.add_note)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = tk.Button(self.button_frame, text="Update", command=self.update_note)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_note)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=0, column=3, padx=5)

    def add_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Input Error", "Title and content cannot be empty.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.add_note(title, content, timestamp)
        self.populate_notes()
        self.clear_fields()

    def update_note(self):
        selected = self.note_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a note to update.")
            return

        index = selected[0]
        note = self.notes[index]
        note_id = note[0]

        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Input Error", "Title and content cannot be empty.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.update_note(note_id, title, content, timestamp)
        self.populate_notes()
        self.clear_fields()

    def delete_note(self):
        selected = self.note_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a note to delete.")
            return

        index = selected[0]
        note = self.notes[index]
        note_id = note[0]

        confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this note?")
        if confirm:
            self.db.delete_note(note_id)
            self.populate_notes()
            self.clear_fields()

    def populate_notes(self):
        self.note_list.delete(0, tk.END)
        self.notes = self.db.get_notes()
        for note in self.notes:
            # note structure: (id, title, content, timestamp)
            self.note_list.insert(tk.END, f"{note[1]} ({note[3]})")

    def on_note_select(self, event):
        selected = self.note_list.curselection()
        if not selected:
            return

        index = selected[0]
        note = self.notes[index]

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note[1])
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(tk.END, note[2])

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.note_list.selection_clear(0, tk.END)

    def on_closing(self):
        self.db.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
