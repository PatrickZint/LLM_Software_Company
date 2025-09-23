import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

import db
import import_export

CONFIG_FILE = 'config.json'

class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Note Taking Application')
        self.geometry('800x600')
        self.db = db.Database(self.get_config().get('database', 'notes.db'))
        self.selected_note_id = None
        self.create_widgets()
        self.refresh_note_list()

    def get_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            return {}

    def create_widgets(self):
        # Top frame for search
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(top_frame, text='Search:').pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        search_entry.bind('<Return>', lambda event: self.search_notes())
        ttk.Button(top_frame, text='Search', command=self.search_notes).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text='Clear', command=self.clear_search).pack(side=tk.LEFT, padx=5)

        # Main frame split: list and detail
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left pane: List of notes
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(left_frame, text='Notes').pack(anchor=tk.W)
        self.notes_listbox = tk.Listbox(left_frame, width=30)
        self.notes_listbox.pack(fill=tk.Y, expand=True, pady=5)
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text='New Note', command=self.new_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text='Delete', command=self.delete_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text='Import', command=self.import_notes).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text='Export', command=self.export_notes).pack(side=tk.LEFT, padx=2)

        # Right pane: Note Details
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right_frame, text='Title:').pack(anchor=tk.W)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(right_frame, textvariable=self.title_var, font=('Arial', 14))
        self.title_entry.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(right_frame, text='Content (Markdown supported):').pack(anchor=tk.W)
        self.content_text = tk.Text(right_frame, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Footer: Save button and timestamps
        footer_frame = ttk.Frame(self)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.info_label = ttk.Label(footer_frame, text='')
        self.info_label.pack(side=tk.LEFT)
        ttk.Button(footer_frame, text='Save', command=self.save_note).pack(side=tk.RIGHT)

    def refresh_note_list(self, notes=None):
        self.notes_listbox.delete(0, tk.END)
        if notes is None:
            notes = self.db.get_all_notes()
        self.notes = notes  # Store list for lookup
        for note in notes:
            # Show title and truncated content
            display = f"{note['title']} - {note['content'][:30].replace('\n', ' ')}..."
            self.notes_listbox.insert(tk.END, display)

    def on_note_select(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            self.selected_note_id = note['id']
            self.title_var.set(note['title'])
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, note['content'])
            created = note.get('created_at', 'N/A')
            updated = note.get('updated_at', 'N/A')
            self.info_label.config(text=f'Created: {created} | Updated: {updated}')

    def new_note(self):
        self.selected_note_id = None
        self.title_var.set('')
        self.content_text.delete(1.0, tk.END)
        self.info_label.config(text='New note (not yet saved)')
        self.notes_listbox.selection_clear(0, tk.END)

    def save_note(self):
        title = self.title_var.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        if not title:
            messagebox.showwarning('Warning', 'Title cannot be empty')
            return

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.selected_note_id is None:
            # New note
            self.db.add_note(title, content, now, now)
            messagebox.showinfo('Info', 'Note added successfully.')
        else:
            # Update existing note
            self.db.update_note(self.selected_note_id, title, content, now)
            messagebox.showinfo('Info', 'Note updated successfully.')

        self.refresh_note_list()
        self.clear_form()

    def delete_note(self):
        if self.selected_note_id is None:
            messagebox.showwarning('Warning', 'No note selected to delete.')
            return
        confirm = messagebox.askyesno('Confirm', 'Are you sure you want to delete this note?')
        if confirm:
            self.db.delete_note(self.selected_note_id)
            messagebox.showinfo('Info', 'Note deleted.')
            self.refresh_note_list()
            self.clear_form()

    def clear_form(self):
        self.selected_note_id = None
        self.title_var.set('')
        self.content_text.delete(1.0, tk.END)
        self.info_label.config(text='')

    def search_notes(self):
        query = self.search_var.get().strip()
        if query:
            notes = self.db.search_notes(query)
            self.refresh_note_list(notes)
        else:
            self.refresh_note_list()

    def clear_search(self):
        self.search_var.set('')
        self.refresh_note_list()

    def export_notes(self):
        export_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON Files', '*.json')])
        if export_path:
            try:
                import_export.export_notes(self.db, export_path)
                messagebox.showinfo('Export', f'Notes exported to {export_path}')
            except Exception as e:
                messagebox.showerror('Error', f'Export failed: {e}')

    def import_notes(self):
        import_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
        if import_path:
            try:
                # Ask the user how to handle duplicates:
                merge = messagebox.askyesno('Import', 'Merge with existing notes? (No will overwrite duplicates)')
                import_export.import_notes(self.db, import_path, merge)
                messagebox.showinfo('Import', 'Notes imported successfully.')
                self.refresh_note_list()
            except Exception as e:
                messagebox.showerror('Error', f'Import failed: {e}')

if __name__ == '__main__':
    app = NoteApp()
    app.mainloop()
