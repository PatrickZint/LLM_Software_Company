import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from database import init_db, get_all_notes, get_note_by_id, create_note, update_note, delete_note


class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Note Taking App")
        self.geometry("800x600")
        self.config_data = self.load_config()
        self.db_path = self.config_data.get("database", "notes.db")
        self.conn = init_db(self.db_path)
        self.create_widgets()
        self.refresh_note_list()

    def load_config(self):
        config_file = "config.json"
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                return json.load(f)
        else:
            messagebox.showerror("Error", "Configuration file not found!")
            self.quit()
            return {}

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame: Note list and buttons
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.note_listbox = tk.Listbox(left_frame, width=40)
        self.note_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.note_listbox.bind('<<ListboxSelect>>', self.on_note_select)

        button_frame = ttk.Frame(left_frame)
        button_frame.pack(side=tk.TOP, pady=10)

        add_button = ttk.Button(button_frame, text="Add New Note", command=self.add_note)
        add_button.pack(side=tk.LEFT, padx=5)

        edit_button = ttk.Button(button_frame, text="Edit Note", command=self.edit_note)
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(button_frame, text="Delete Note", command=self.delete_note)
        delete_button.pack(side=tk.LEFT, padx=5)

        # Right frame: Note details
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.note_detail = tk.Text(right_frame, wrap=tk.WORD)
        self.note_detail.pack(fill=tk.BOTH, expand=True)
        self.note_detail.config(state=tk.DISABLED)

    def refresh_note_list(self):
        self.note_listbox.delete(0, tk.END)
        self.notes = get_all_notes(self.conn)
        for note in self.notes:
            # note tuple: (id, title, content, created_timestamp, updated_timestamp)
            display_text = f"{note[1]} ({note[3]})"
            self.note_listbox.insert(tk.END, display_text)

        # Clear the note detail pane
        self.note_detail.config(state=tk.NORMAL)
        self.note_detail.delete("1.0", tk.END)
        self.note_detail.config(state=tk.DISABLED)

    def on_note_select(self, event):
        selection = self.note_listbox.curselection()
        if selection:
            index = selection[0]
            note_id = self.notes[index][0]
            note = get_note_by_id(self.conn, note_id)
            if note:
                self.note_detail.config(state=tk.NORMAL)
                self.note_detail.delete("1.0", tk.END)
                info = (
                    f"Title: {note[1]}\n"
                    f"Created: {note[3]}\n"
                    f"Updated: {note[4]}\n\n"
                    f"Content:\n{note[2]}"
                )
                self.note_detail.insert(tk.END, info)
                self.note_detail.config(state=tk.DISABLED)

    def add_note(self):
        NoteEditor(self, self.conn, mode="add", refresh_callback=self.refresh_note_list)

    def edit_note(self):
        selection = self.note_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a note to edit.")
            return
        index = selection[0]
        note_id = self.notes[index][0]
        NoteEditor(self, self.conn, mode="edit", note_id=note_id, refresh_callback=self.refresh_note_list)

    def delete_note(self):
        selection = self.note_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a note to delete.")
            return
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this note?")
        if confirm:
            index = selection[0]
            note_id = self.notes[index][0]
            delete_note(self.conn, note_id)
            self.refresh_note_list()


class NoteEditor(tk.Toplevel):
    def __init__(self, master, conn, mode, refresh_callback, note_id=None):
        super().__init__(master)
        self.conn = conn
        self.mode = mode  # "add" or "edit"
        self.refresh_callback = refresh_callback
        self.note_id = note_id
        self.title("Add Note" if mode == "add" else "Edit Note")
        self.geometry("400x300")
        self.create_widgets()
        if self.mode == "edit":
            self.load_note_data()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title label and entry
        title_label = ttk.Label(frame, text="Title:")
        title_label.pack(anchor=tk.W)
        self.title_entry = ttk.Entry(frame)
        self.title_entry.pack(fill=tk.X)

        # Content label and text widget
        content_label = ttk.Label(frame, text="Content:")
        content_label.pack(anchor=tk.W, pady=(10, 0))
        self.content_text = tk.Text(frame, height=10, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # Save button
        save_button = ttk.Button(frame, text="Save", command=self.save_note)
        save_button.pack(pady=10)

    def load_note_data(self):
        note = get_note_by_id(self.conn, self.note_id)
        if note:
            self.title_entry.insert(0, note[1])
            self.content_text.insert("1.0", note[2])

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        if not title:
            messagebox.showerror("Error", "Title cannot be empty.")
            return
        if self.mode == "add":
            create_note(self.conn, title, content)
        elif self.mode == "edit":
            update_note(self.conn, self.note_id, title, content)
        self.refresh_callback()
        self.destroy()


if __name__ == "__main__":
    app = NoteApp()
    app.mainloop()
