import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from database import NoteDatabase
import os
import json

class NotesApp(tk.Tk):
    def __init__(self, db, config):
        super().__init__()
        self.title("Note-Taking Application")
        self.geometry("800x600")
        self.db = db
        self.config_data = config

        # Left frame: list of notes and search
        self.left_frame = tk.Frame(self, width=250)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.left_frame, textvariable=self.search_var)
        self.search_entry.pack(padx=5, pady=5, fill=tk.X)
        self.search_entry.bind('<Return>', lambda event: self.perform_search())

        self.notes_listbox = tk.Listbox(self.left_frame)
        self.notes_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.notes_listbox.bind('<<ListboxSelect>>', lambda event: self.load_selected_note())

        # Buttons on left frame
        btn_frame = tk.Frame(self.left_frame)
        btn_frame.pack(padx=5, pady=5, fill=tk.X)
        tk.Button(btn_frame, text="New Note", command=self.new_note).pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Button(btn_frame, text="Delete", command=self.delete_note).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Right frame: note details and editor
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title
        title_frame = tk.Frame(self.right_frame)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(title_frame, text="Title:").pack(side=tk.LEFT)
        self.title_entry = tk.Entry(title_frame)
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Categories and Tags
        meta_frame = tk.Frame(self.right_frame)
        meta_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(meta_frame, text="Categories:").pack(side=tk.LEFT)
        self.categories_entry = tk.Entry(meta_frame, width=20)
        self.categories_entry.pack(side=tk.LEFT, padx=(0,10))
        tk.Label(meta_frame, text="Tags:").pack(side=tk.LEFT)
        self.tags_entry = tk.Entry(meta_frame, width=20)
        self.tags_entry.pack(side=tk.LEFT)

        # Toolbar for rich text formatting
        toolbar = tk.Frame(self.right_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(toolbar, text="Bold", command=self.make_bold).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Italic", command=self.make_italic).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Underline", command=self.make_underline).pack(side=tk.LEFT, padx=2)

        # Text Editor (supports Markdown formatting by inserting markdown symbols)
        editor_settings = self.config_data.get("EditorSettings", {})
        font_size = editor_settings.get("FontSize", 14)
        font_family = editor_settings.get("FontFamily", "Helvetica")
        self.text_editor = tk.Text(self.right_frame, wrap=tk.WORD, font=(font_family, font_size))
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Bottom Buttons
        bottom_frame = tk.Frame(self.right_frame)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(bottom_frame, text="Save Note", command=self.save_note).pack(side=tk.LEFT, padx=2)
        tk.Button(bottom_frame, text="Export Notes", command=self.export_notes).pack(side=tk.LEFT, padx=2)
        tk.Button(bottom_frame, text="Import Notes", command=self.import_notes).pack(side=tk.LEFT, padx=2)

        self.current_note_id = None
        self.refresh_notes_list()

    def refresh_notes_list(self, notes=None):
        self.notes_listbox.delete(0, tk.END)
        if notes is None:
            notes = self.db.get_all_notes()
        self.notes = notes  # store current list
        for note in notes:
            display_text = f"{note['title']} - {note['created_at'][:19]}"
            self.notes_listbox.insert(tk.END, display_text)

    def load_selected_note(self):
        try:
            index = self.notes_listbox.curselection()[0]
        except IndexError:
            return
        note = self.notes[index]
        self.current_note_id = note['id']
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note['title'])
        self.categories_entry.delete(0, tk.END)
        self.categories_entry.insert(0, note.get('categories', ''))
        self.tags_entry.delete(0, tk.END)
        self.tags_entry.insert(0, note.get('tags', ''))
        self.text_editor.delete('1.0', tk.END)
        self.text_editor.insert(tk.END, note['content'])

    def new_note(self):
        # Clear the editor fields for a new note
        self.current_note_id = None
        self.title_entry.delete(0, tk.END)
        self.categories_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)
        self.text_editor.delete('1.0', tk.END)
        self.notes_listbox.selection_clear(0, tk.END)

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.text_editor.get('1.0', tk.END).strip()
        categories = self.categories_entry.get().strip()
        tags = self.tags_entry.get().strip()
        
        if not title or not content:
            messagebox.showwarning("Validation Error", "Title and content cannot be empty.")
            return
        
        if self.current_note_id:
            self.db.update_note(self.current_note_id, title, content, categories, tags)
            messagebox.showinfo("Success", "Note updated successfully.")
        else:
            self.db.add_note(title, content, categories, tags)
            messagebox.showinfo("Success", "Note created successfully.")
        self.refresh_notes_list()

    def delete_note(self):
        if not self.current_note_id:
            messagebox.showwarning("Delete Note", "No note selected.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
            self.db.delete_note(self.current_note_id)
            self.new_note()
            self.refresh_notes_list()

    def perform_search(self):
        keyword = self.search_var.get().strip()
        if keyword == "":
            notes = self.db.get_all_notes()
        else:
            notes = self.db.search_notes(keyword)
        self.refresh_notes_list(notes)

    def export_notes(self):
        export_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if export_path:
            try:
                self.db.export_notes(export_path)
                messagebox.showinfo("Export", f"Notes exported to {export_path}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def import_notes(self):
        import_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if import_path:
            try:
                self.db.import_notes(import_path)
                messagebox.showinfo("Import", f"Notes imported from {import_path}")
                self.refresh_notes_list()
            except Exception as e:
                messagebox.showerror("Import Error", str(e))

    # Rich Text Formatting Functions
    def get_selected_text_range(self):
        try:
            start = self.text_editor.index("sel.first")
            end = self.text_editor.index("sel.last")
            return start, end
        except tk.TclError:
            return None, None

    def wrap_selection(self, wrapper):
        start, end = self.get_selected_text_range()
        if start and end:
            selected_text = self.text_editor.get(start, end)
            new_text = f"{wrapper}{selected_text}{wrapper}"
            self.text_editor.delete(start, end)
            self.text_editor.insert(start, new_text)
        else:
            messagebox.showinfo("Selection Required", "Please select text to format.")

    def make_bold(self):
        self.wrap_selection("**")

    def make_italic(self):
        self.wrap_selection("*")

    def make_underline(self):
        # In Markdown there isn't a default underline syntax, using HTML style for example
        start, end = self.get_selected_text_range()
        if start and end:
            selected_text = self.text_editor.get(start, end)
            # Using HTML underline tag
            new_text = f"<u>{selected_text}</u>"
            self.text_editor.delete(start, end)
            self.text_editor.insert(start, new_text)
        else:
            messagebox.showinfo("Selection Required", "Please select text to format.")
