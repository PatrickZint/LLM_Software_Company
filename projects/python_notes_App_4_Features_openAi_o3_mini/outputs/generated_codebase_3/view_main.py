import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from note_controller import NoteController
from config_manager import ConfigManager


class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.controller = NoteController()
        self.config_manager = ConfigManager()
        self.create_widgets()
        self.load_notes()

    def create_widgets(self):
        # Header Frame for navigation buttons
        self.header_frame = tk.Frame(self, height=50, bg='lightgray')
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        # Sidebar Frame for filters (e.g., categories, tags)
        self.sidebar_frame = tk.Frame(self, width=200, bg='white')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Main Frame for list view and detailed editor
        self.main_frame = tk.Frame(self, bg='white')
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Header buttons
        self.btn_create = tk.Button(self.header_frame, text='Create Note', command=self.create_note)
        self.btn_create.pack(side=tk.LEFT, padx=5, pady=10)
        self.btn_export = tk.Button(self.header_frame, text='Export', command=self.export_notes)
        self.btn_export.pack(side=tk.LEFT, padx=5, pady=10)
        self.btn_import = tk.Button(self.header_frame, text='Import', command=self.import_notes)
        self.btn_import.pack(side=tk.LEFT, padx=5, pady=10)

        # Sidebar content (example: Filter label)
        self.lbl_filter = tk.Label(self.sidebar_frame, text='Filters', bg='white')
        self.lbl_filter.pack(padx=10, pady=10)
        # You can extend this section with dropdowns or entry widgets for filtering

        # In the main frame, split into a list of notes and an editor pane
        self.list_frame = tk.Frame(self.main_frame, bg='white')
        self.list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.note_list = tk.Listbox(self.list_frame, width=30)
        self.note_list.pack(side=tk.TOP, fill=tk.Y, expand=True)
        self.note_list.bind('<<ListboxSelect>>', self.on_note_select)

        # Editor panel
        self.editor_frame = tk.Frame(self.main_frame, bg='white')
        self.editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.txt_editor = tk.Text(self.editor_frame)
        self.txt_editor.pack(fill=tk.BOTH, expand=True)

        # Save and Delete buttons
        self.btn_save = tk.Button(self.editor_frame, text='Save', command=self.save_note)
        self.btn_save.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_delete = tk.Button(self.editor_frame, text='Delete', command=self.delete_note)
        self.btn_delete.pack(side=tk.LEFT, padx=5, pady=5)

    def load_notes(self):
        self.note_list.delete(0, tk.END)
        self.notes = self.controller.get_all_notes()
        for note in self.notes:
            self.note_list.insert(tk.END, f"{note['id']}: {note['title']}")

    def on_note_select(self, event):
        selection = self.note_list.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            self.txt_editor.delete('1.0', tk.END)
            self.txt_editor.insert(tk.END, note['content'])
            self.current_note_id = note['id']
        else:
            self.current_note_id = None

    def create_note(self):
        title = 'New Note'
        content = ''
        note_id = self.controller.create_note(title, content)
        self.load_notes()
        messagebox.showinfo('Info', 'Note created successfully')

    def save_note(self):
        if hasattr(self, 'current_note_id') and self.current_note_id:
            content = self.txt_editor.get('1.0', tk.END)
            self.controller.update_note(self.current_note_id, content=content)
            self.load_notes()
            messagebox.showinfo('Info', 'Note updated successfully')
        else:
            messagebox.showwarning('Warning', 'No note selected')

    def delete_note(self):
        if hasattr(self, 'current_note_id') and self.current_note_id:
            if messagebox.askyesno('Confirm', 'Are you sure you want to delete this note?'):
                self.controller.delete_note(self.current_note_id)
                self.load_notes()
                self.txt_editor.delete('1.0', tk.END)
        else:
            messagebox.showwarning('Warning', 'No note selected')

    def export_notes(self):
        filepath = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON Files', '*.json')])
        if filepath:
            success = self.controller.export_notes(filepath)
            if success:
                messagebox.showinfo('Export', 'Notes exported successfully')
            else:
                messagebox.showerror('Export', 'Failed to export notes')
    
    def import_notes(self):
        filepath = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
        if filepath:
            success = self.controller.import_notes(filepath)
            if success:
                self.load_notes()
                messagebox.showinfo('Import', 'Notes imported successfully')
            else:
                messagebox.showerror('Import', 'Failed to import notes')
