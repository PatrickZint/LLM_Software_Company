import tkinter as tk
from tkinter import messagebox, filedialog
import json

from database import Database


class NoteApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.selected_note_id = None
        
        self.build_ui()
        self.load_notes()
    
    def build_ui(self):
        # Search Bar
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, pady=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        tk.Button(search_frame, text="Search", command=self.search_notes).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Clear", command=self.load_notes).pack(side=tk.LEFT, padx=5)
        
        # Note List
        list_frame = tk.Frame(self.root)
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.note_listbox = tk.Listbox(list_frame, width=30)
        self.note_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.note_listbox.bind("<<ListboxSelect>>", self.on_note_select)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.config(command=self.note_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.note_listbox.config(yscrollcommand=scrollbar.set)
        
        # Note Details
        detail_frame = tk.Frame(self.root)
        detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.detail_text = tk.Text(detail_frame, wrap=tk.WORD)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # Action Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="Add Note", command=self.add_note).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit Note", command=self.edit_note).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Note", command=self.delete_note).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Export", command=self.export_notes).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Import", command=self.import_notes).pack(side=tk.LEFT, padx=5)
    
    def load_notes(self):
        self.note_listbox.delete(0, tk.END)
        self.notes = self.db.get_all_notes()
        for note in self.notes:
            display_text = f"{note['title']} ({note['timestamp']})"
            self.note_listbox.insert(tk.END, display_text)
        self.detail_text.delete(1.0, tk.END)
        self.selected_note_id = None
    
    def on_note_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            self.selected_note_id = note['id']
            display = (
                f"Title: {note['title']}\n"
                f"Timestamp: {note['timestamp']}\n"
                f"Categories: {note.get('categories', '')}\n"
                f"Tags: {note.get('tags', '')}\n\n"
                f"{note['content']}"
            )
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, display)
        else:
            self.selected_note_id = None
    
    def add_note(self):
        self.note_editor()
    
    def edit_note(self):
        if self.selected_note_id is None:
            messagebox.showwarning("Select Note", "Please select a note to edit.")
            return
        note = next((n for n in self.notes if n["id"] == self.selected_note_id), None)
        if note:
            self.note_editor(note)
    
    def note_editor(self, note=None):
        editor = tk.Toplevel(self.root)
        editor.title("Note Editor")
        
        tk.Label(editor, text="Title").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        title_var = tk.StringVar(value=note["title"] if note else "")
        title_entry = tk.Entry(editor, textvariable=title_var, width=50)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(editor, text="Categories").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        cat_var = tk.StringVar(value=note.get("categories", "") if note else "")
        cat_entry = tk.Entry(editor, textvariable=cat_var, width=50)
        cat_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(editor, text="Tags").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        tag_var = tk.StringVar(value=note.get("tags", "") if note else "")
        tag_entry = tk.Entry(editor, textvariable=tag_var, width=50)
        tag_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(editor, text="Content (Markdown supported)").grid(row=3, column=0, sticky=tk.NW, padx=5, pady=5)
        content_text = tk.Text(editor, width=60, height=20, wrap=tk.WORD)
        content_text.grid(row=3, column=1, padx=5, pady=5)
        if note:
            content_text.insert(tk.END, note["content"])
        
        # Simple formatting toolbar
        toolbar = tk.Frame(editor)
        toolbar.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        tk.Button(toolbar, text="Bold", command=lambda: self.add_formatting(content_text, "**")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Italic", command=lambda: self.add_formatting(content_text, "_")).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Heading", command=lambda: self.add_formatting(content_text, "#")).pack(side=tk.LEFT, padx=2)
        
        def save_note():
            title = title_var.get()
            content = content_text.get(1.0, tk.END).strip()
            categories = cat_var.get()
            tags = tag_var.get()
            if not title:
                messagebox.showwarning("Missing Title", "Title cannot be empty.")
                return
            if note:
                self.db.update_note(note["id"], title, content, categories, tags)
            else:
                self.db.add_note(title, content, categories, tags)
            self.load_notes()
            editor.destroy()
        
        tk.Button(editor, text="Save", command=save_note).grid(row=5, column=1, pady=10)
    
    def add_formatting(self, text_widget, markup):
        try:
            start = text_widget.index("sel.first")
            end = text_widget.index("sel.last")
            selected_text = text_widget.get(start, end)
            formatted = f"{markup}{selected_text}{markup}"
            text_widget.delete(start, end)
            text_widget.insert(start, formatted)
        except tk.TclError:
            messagebox.showinfo("No Selection", "Select text to apply formatting.")
    
    def delete_note(self):
        if self.selected_note_id is None:
            messagebox.showwarning("Select Note", "No note selected.")
            return
        if messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?"):
            self.db.delete_note(self.selected_note_id)
            self.load_notes()
            self.detail_text.delete(1.0, tk.END)
            self.selected_note_id = None
    
    def export_notes(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON Files", "*.json")])
        if file_path:
            notes = self.db.export_notes()
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(notes, f, indent=4)
                messagebox.showinfo("Export", "Notes exported successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export notes: {e}")
    
    def import_notes(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    notes = json.load(f)
                self.db.import_notes(notes)
                self.load_notes()
                messagebox.showinfo("Import", "Notes imported successfully.")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import notes: {e}")
    
    def search_notes(self):
        keyword = self.search_var.get()
        if keyword:
            self.note_listbox.delete(0, tk.END)
            self.notes = self.db.search_notes(keyword)
            for note in self.notes:
                display_text = f"{note['title']} ({note['timestamp']})"
                self.note_listbox.insert(tk.END, display_text)
        else:
            self.load_notes()
