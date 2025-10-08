import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from database import NoteDatabase
from models import Note
from datetime import datetime

# Load configuration
CONFIG_FILE = 'config.json'
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
else:
    config = {}

DB_PATH = config.get('DatabaseFilePath', 'notes.db')
DEFAULT_EXPORT_PATH = config.get('DefaultExportPath', './')

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

class NoteApp:
    def __init__(self, master):
        self.master = master
        master.title('Note Taking Application')
        
        self.db = NoteDatabase(DB_PATH)
        
        # Current selected note id
        self.current_note_id = None

        # Layout frames: left for list; right for detail/edit
        self.left_frame = tk.Frame(master, padx=5, pady=5)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.right_frame = tk.Frame(master, padx=5, pady=5)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left Frame: Listbox for notes + scrollbar
        self.note_listbox = tk.Listbox(self.left_frame, width=30)
        self.note_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.note_listbox.bind('<<ListboxSelect>>', self.on_note_select)

        self.list_scrollbar = tk.Scrollbar(self.left_frame, orient=tk.VERTICAL)
        self.list_scrollbar.config(command=self.note_listbox.yview)
        self.list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.note_listbox.config(yscrollcommand=self.list_scrollbar.set)

        # Right Frame: Form for note details
        self.title_label = tk.Label(self.right_frame, text='Title:')
        self.title_label.pack(anchor='w')
        self.title_entry = tk.Entry(self.right_frame, width=50)
        self.title_entry.pack(fill=tk.X)

        self.content_label = tk.Label(self.right_frame, text='Content:')
        self.content_label.pack(anchor='w')
        self.content_text = tk.Text(self.right_frame, height=15)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # Categories and Tags
        self.cat_label = tk.Label(self.right_frame, text='Categories (comma separated):')
        self.cat_label.pack(anchor='w')
        self.cat_entry = tk.Entry(self.right_frame, width=50)
        self.cat_entry.pack(fill=tk.X)

        self.tag_label = tk.Label(self.right_frame, text='Tags (comma separated):')
        self.tag_label.pack(anchor='w')
        self.tag_entry = tk.Entry(self.right_frame, width=50)
        self.tag_entry.pack(fill=tk.X)

        # Buttons
        self.button_frame = tk.Frame(self.right_frame, pady=10)
        self.button_frame.pack(fill=tk.X)

        self.new_button = tk.Button(self.button_frame, text='New Note', command=self.new_note)
        self.new_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.button_frame, text='Save Note', command=self.save_note)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text='Delete Note', command=self.delete_note)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.import_button = tk.Button(self.button_frame, text='Import Notes', command=self.import_notes)
        self.import_button.pack(side=tk.LEFT, padx=5)

        self.export_button = tk.Button(self.button_frame, text='Export Notes', command=self.export_notes)
        self.export_button.pack(side=tk.LEFT, padx=5)

        self.refresh_notes_list()

    def refresh_notes_list(self):
        self.note_listbox.delete(0, tk.END)
        self.notes = self.db.get_all_notes()
        for note in self.notes:
            # Show title and created_at date as preview
            display_text = f"{note.title} - {note.created_at.split('T')[0]}"
            self.note_listbox.insert(tk.END, display_text)

    def on_note_select(self, event):
        if not self.note_listbox.curselection():
            return
        index = self.note_listbox.curselection()[0]
        note = self.notes[index]
        self.current_note_id = note.id

        # Populate fields with note data
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note.title)
        
        self.content_text.delete('1.0', tk.END)
        self.content_text.insert(tk.END, note.content)
        
        self.cat_entry.delete(0, tk.END)
        self.cat_entry.insert(0, note.categories)
        
        self.tag_entry.delete(0, tk.END)
        self.tag_entry.insert(0, note.tags)

    def new_note(self):
        self.current_note_id = None
        self.title_entry.delete(0, tk.END)
        self.content_text.delete('1.0', tk.END)
        self.cat_entry.delete(0, tk.END)
        self.tag_entry.delete(0, tk.END)
        self.note_listbox.selection_clear(0, tk.END)

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()
        categories = self.cat_entry.get().strip()
        tags = self.tag_entry.get().strip()
        
        if not title or not content:
            messagebox.showwarning('Missing Data', 'Title and content are required.')
            return
        
        now = datetime.now().isoformat()

        if self.current_note_id is None:
            # New note
            note = Note(
                id=None,
                title=title,
                content=content,
                created_at=now,
                updated_at=now,
                categories=categories,
                tags=tags
            )
            note_id = self.db.add_note(note)
            self.current_note_id = note_id
        else:
            # Update existing note
            note = Note(
                id=self.current_note_id,
                title=title,
                content=content,
                created_at=now,  # not used for update
                updated_at=now,
                categories=categories,
                tags=tags
            )
            self.db.update_note(note)
        
        self.refresh_notes_list()
        messagebox.showinfo('Success', 'Note saved successfully.')

    def delete_note(self):
        if self.current_note_id is None:
            messagebox.showwarning('No Selection', 'Please select a note to delete.')
            return
        answer = messagebox.askyesno('Confirm Delete', 'Are you sure you want to delete this note?')
        if answer:
            self.db.delete_note(self.current_note_id)
            self.new_note()
            self.refresh_notes_list()
            messagebox.showinfo('Deleted', 'Note deleted successfully.')

    def import_notes(self):
        file_path = filedialog.askopenfilename(title='Import Notes', filetypes=[('JSON Files', '*.json')])
        if file_path:
            try:
                self.db.import_notes(file_path)
                self.refresh_notes_list()
                messagebox.showinfo('Import', 'Notes imported successfully.')
            except Exception as e:
                messagebox.showerror('Import Error', f'Failed to import notes: {e}')

    def export_notes(self):
        file_path = filedialog.asksaveasfilename(title='Export Notes', defaultextension='.json', initialdir=DEFAULT_EXPORT_PATH, filetypes=[('JSON Files', '*.json')])
        if file_path:
            try:
                self.db.export_notes(file_path)
                messagebox.showinfo('Export', 'Notes exported successfully.')
            except Exception as e:
                messagebox.showerror('Export Error', f'Failed to export notes: {e}')

    def on_close(self):
        self.db.close()
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = NoteApp(root)
    root.protocol('WM_DELETE_WINDOW', app.on_close)
    root.mainloop()
