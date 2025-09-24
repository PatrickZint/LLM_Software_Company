import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from note_manager import NoteManager

class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Simple Note-Taking Application')
        self.geometry('600x400')
        
        # Initialize the note manager
        self.note_manager = NoteManager()
        
        # Set up the UI
        self.create_widgets()
        self.populate_notes_list()

    def create_widgets(self):
        # Frames
        self.left_frame = ttk.Frame(self, width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Listbox for notes
        self.notes_listbox = tk.Listbox(self.left_frame)
        self.notes_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)
        
        # Buttons on left frame
        self.btn_new = ttk.Button(self.left_frame, text='New Note', command=self.new_note)
        self.btn_new.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        self.btn_delete = ttk.Button(self.left_frame, text='Delete Note', command=self.delete_note)
        self.btn_delete.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        # Note form in right frame
        self.form_frame = ttk.Frame(self.right_frame)
        self.form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.form_frame, text='Title:').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_title = ttk.Entry(self.form_frame)
        self.entry_title.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(self.form_frame, text='Content:').grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        self.text_content = tk.Text(self.form_frame, height=10)
        self.text_content.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        self.form_frame.columnconfigure(1, weight=1)

        # Save button
        self.btn_save = ttk.Button(self.right_frame, text='Save Note', command=self.save_note)
        self.btn_save.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
    def populate_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        for note in self.note_manager.get_all_notes():
            display_text = f"{note['title']} (Last updated: {note['timestamp']})"
            self.notes_listbox.insert(tk.END, display_text)

    def on_note_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            note = self.note_manager.get_all_notes()[index]
            self.display_note(note)

    def display_note(self, note):
        self.current_note_id = note['id']
        self.entry_title.delete(0, tk.END)
        self.entry_title.insert(0, note['title'])
        
        self.text_content.delete('1.0', tk.END)
        self.text_content.insert(tk.END, note['content'])

    def new_note(self):
        # Clear the form for a new note
        self.current_note_id = None
        self.entry_title.delete(0, tk.END)
        self.text_content.delete('1.0', tk.END)
        self.notes_listbox.selection_clear(0, tk.END)

    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.text_content.get('1.0', tk.END).strip()
        
        if not title:
            messagebox.showerror('Error', 'Title cannot be empty.')
            return

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if self.current_note_id is None:
            # Create new note
            self.note_manager.create_note(title, content, timestamp)
            messagebox.showinfo('Success', 'Note created successfully.')
        else:
            # Edit existing note
            self.note_manager.edit_note(self.current_note_id, title, content, timestamp)
            messagebox.showinfo('Success', 'Note updated successfully.')

        self.note_manager.save_notes()
        self.populate_notes_list()

    def delete_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showerror('Error', 'Please select a note to delete.')
            return
        index = selection[0]
        note = self.note_manager.get_all_notes()[index]
        
        confirm = messagebox.askyesno('Confirm Deletion', f"Are you sure you want to delete '{note['title']}'?")
        if confirm:
            self.note_manager.delete_note(note['id'])
            self.note_manager.save_notes()
            messagebox.showinfo('Success', 'Note deleted successfully.')
            self.new_note()
            self.populate_notes_list()

if __name__ == '__main__':
    app = NoteApp()
    app.mainloop()
