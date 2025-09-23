import tkinter as tk
from tkinter import messagebox
from note_model import Note


class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Note Taking App")
        self.geometry("600x400")
        
        # Left frame for list of notes
        self.list_frame = tk.Frame(self)
        self.list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.listbox = tk.Listbox(self.list_frame, width=40)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.bind("<<ListboxSelect>>", self.on_note_select)

        # Add a scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right frame for note details and action buttons
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Text widget to display selected note details
        self.text = tk.Text(self.right_frame)
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # Frame for action buttons
        self.button_frame = tk.Frame(self.right_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        self.add_button = tk.Button(self.button_frame, text="Add Note", command=self.open_add_note)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = tk.Button(self.button_frame, text="Edit Note", command=self.open_edit_note)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Note", command=self.delete_note)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Currently selected note id
        self.selected_note_id = None

        # Load all notes into the listbox
        self.refresh_notes()

    def refresh_notes(self):
        """
        Refresh the list of notes displayed in the listbox.
        """
        self.listbox.delete(0, tk.END)
        notes = Note.get_all()
        for note in notes:
            display = f"{note.id}: {note.title} ({note.created_at[:10]})"
            self.listbox.insert(tk.END, display)

    def on_note_select(self, event):
        """
        Handle note selection from the listbox and display its details.
        """
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            item_text = self.listbox.get(index)
            # Assume the id is before the colon
            note_id = int(item_text.split(":")[0])
            note = Note.get_by_id(note_id)
            if note:
                self.selected_note_id = note.id
                self.text.delete('1.0', tk.END)
                self.text.insert(tk.END, f"Title: {note.title}\n")
                self.text.insert(tk.END, f"Created: {note.created_at}\n")
                self.text.insert(tk.END, f"Updated: {note.updated_at}\n")
                self.text.insert(tk.END, "\nContent:\n")
                self.text.insert(tk.END, note.content)
        else:
            self.selected_note_id = None
            self.text.delete('1.0', tk.END)

    def open_add_note(self):
        """ Open the NoteForm for adding a new note. """
        NoteForm(self, mode="add")

    def open_edit_note(self):
        """ Open the NoteForm pre-filled with the selected note for editing. """
        if self.selected_note_id:
            note = Note.get_by_id(self.selected_note_id)
            if note:
                NoteForm(self, mode="edit", note=note)
        else:
            messagebox.showinfo("Info", "Please select a note to edit.")

    def delete_note(self):
        """ Delete the selected note after user confirmation. """
        if self.selected_note_id:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
                Note.delete(self.selected_note_id)
                self.selected_note_id = None
                self.refresh_notes()
                self.text.delete('1.0', tk.END)
        else:
            messagebox.showinfo("Info", "Please select a note to delete.")


class NoteForm(tk.Toplevel):
    def __init__(self, master, mode="add", note=None):
        super().__init__(master)
        self.master = master
        self.mode = mode
        self.note = note
        self.title("Add Note" if mode == "add" else "Edit Note")

        # Title input
        tk.Label(self, text="Title:").pack(pady=5)
        self.title_entry = tk.Entry(self, width=50)
        self.title_entry.pack(padx=10)

        # Content input
        tk.Label(self, text="Content:").pack(pady=5)
        self.content_text = tk.Text(self, width=50, height=10)
        self.content_text.pack(padx=10)

        # Save button
        self.save_button = tk.Button(self, text="Save", command=self.save_note)
        self.save_button.pack(pady=10)

        # If editing an existing note, populate the fields
        if self.mode == "edit" and self.note:
            self.title_entry.insert(0, self.note.title)
            self.content_text.insert('1.0', self.note.content)

    def save_note(self):
        """ Validate input and save the note (either create or update). """
        title = self.title_entry.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()

        if not title or not content:
            messagebox.showerror("Error", "Both title and content are required!")
            return

        if len(title) > 100:
            messagebox.showerror("Error", "Title must be at most 100 characters long.")
            return

        if self.mode == "add":
            Note.create(title, content)
        elif self.mode == "edit":
            Note.update(self.note.id, title, content)

        # Refresh the main list and close the form
        self.master.refresh_notes()
        self.destroy()