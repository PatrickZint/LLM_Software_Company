import tkinter as tk
from tkinter import ttk, messagebox
from note import Note
from database import NoteDatabase
from exporter import export_notes, import_notes


class NoteAppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taking App")
        self.db = NoteDatabase()

        self.create_widgets()
        self.populate_notes()

    def create_widgets(self):
        # Search Frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_notes).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Reset", command=self.populate_notes).pack(side=tk.LEFT)

        # Main Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # List of Notes
        self.notes_listbox = tk.Listbox(main_frame)
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)

        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        ttk.Button(button_frame, text="New Note", command=self.new_note).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Edit Note", command=self.edit_note).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Delete Note", command=self.delete_note).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Export Notes", command=self.export_notes_ui).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Import Notes", command=self.import_notes_ui).pack(fill=tk.X, pady=2)

        # Note Detail Frame
        self.detail_frame = ttk.Frame(self.root)
        self.detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(self.detail_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(self.detail_frame, textvariable=self.title_var, width=50)
        self.title_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.detail_frame, text="Category:").grid(row=1, column=0, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_entry = ttk.Entry(self.detail_frame, textvariable=self.category_var, width=50)
        self.category_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.detail_frame, text="Tags (comma separated):").grid(row=2, column=0, sticky=tk.W)
        self.tags_var = tk.StringVar()
        self.tags_entry = ttk.Entry(self.detail_frame, textvariable=self.tags_var, width=50)
        self.tags_entry.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(self.detail_frame, text="Content:").grid(row=3, column=0, sticky=tk.NW)
        self.content_text = tk.Text(self.detail_frame, width=50, height=10)
        self.content_text.grid(row=3, column=1, sticky=tk.W)

        # Save Button
        self.save_button = ttk.Button(self.detail_frame, text="Save Note", command=self.save_note)
        self.save_button.grid(row=4, column=1, sticky=tk.E, pady=5)

        # Currently selected note id
        self.current_note_id = None

    def populate_notes(self):
        self.notes_listbox.delete(0, tk.END)
        self.notes = self.db.get_all_notes()
        for note in self.notes:
            display_text = f"{note.title} - {note.created_at}"
            self.notes_listbox.insert(tk.END, display_text)
        # Clear detail form
        self.clear_form()

    def search_notes(self):
        keyword = self.search_var.get()
        self.notes_listbox.delete(0, tk.END)
        self.notes = self.db.search_notes(keyword)
        for note in self.notes:
            display_text = f"{note.title} - {note.created_at}"
            self.notes_listbox.insert(tk.END, display_text)
        self.clear_form()

    def on_note_select(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            self.populate_form(note)

    def populate_form(self, note):
        self.current_note_id = note.id
        self.title_var.set(note.title)
        self.category_var.set(note.category)
        self.tags_var.set(note.tags)
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(tk.END, note.content)

    def clear_form(self):
        self.current_note_id = None
        self.title_var.set("")
        self.category_var.set("")
        self.tags_var.set("")
        self.content_text.delete(1.0, tk.END)

    def new_note(self):
        self.clear_form()

    def save_note(self):
        title = self.title_var.get()
        content = self.content_text.get(1.0, tk.END).strip()
        category = self.category_var.get()
        tags = self.tags_var.get()

        if not title or not content:
            messagebox.showerror("Error", "Title and Content are required.")
            return

        if self.current_note_id:
            # Update existing note
            note = self.db.get_note_by_id(self.current_note_id)
            note.title = title
            note.content = content
            note.category = category
            note.tags = tags
            self.db.update_note(note)
            messagebox.showinfo("Info", "Note updated successfully.")
        else:
            # Create new note
            note = Note(title=title, content=content, category=category, tags=tags)
            self.db.add_note(note)
            messagebox.showinfo("Info", "Note created successfully.")

        self.populate_notes()

    def edit_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a note to edit.")
            return
        # Form is already populated via on_note_select
        messagebox.showinfo("Info", "Edit the fields and click 'Save Note'.")

    def delete_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a note to delete.")
            return
        index = selection[0]
        note = self.notes[index]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete note: {note.title}?")
        if confirm:
            self.db.delete_note(note.id)
            messagebox.showinfo("Info", "Note deleted successfully.")
            self.populate_notes()

    def export_notes_ui(self):
        notes = self.db.get_all_notes()
        export_notes(notes)
        messagebox.showinfo("Export", "Notes exported successfully.")

    def import_notes_ui(self):
        imported_notes = import_notes()
        for note in imported_notes:
            # Only add if the note doesn't already exist (simple check: by title and creation time)
            existing = self.db.search_notes(note.title)
            if not existing:
                self.db.add_note(note)
        messagebox.showinfo("Import", "Notes imported successfully.")
        self.populate_notes()

    def on_close(self):
        self.db.close()
        self.root.destroy()
