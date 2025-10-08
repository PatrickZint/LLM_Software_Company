import tkinter as tk
from tkinter import messagebox, simpledialog

class NoteTakingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Note Taking App")
        self.notes = []  # Each note will be a dict: {'title': str, 'content': str}
        
        # Frame for the listbox and scrollbar
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)
        
        self.note_listbox = tk.Listbox(frame, width=50, height=15)
        self.note_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.note_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.note_listbox.config(yscrollcommand=scrollbar.set)

        # Buttons frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        add_btn = tk.Button(btn_frame, text="Add Note", command=self.add_note)
        add_btn.grid(row=0, column=0, padx=5)

        edit_btn = tk.Button(btn_frame, text="Edit Note", command=self.edit_note)
        edit_btn.grid(row=0, column=1, padx=5)

        delete_btn = tk.Button(btn_frame, text="Delete Note", command=self.delete_note)
        delete_btn.grid(row=0, column=2, padx=5)

        # Bind double-click on listbox to view/edit note
        self.note_listbox.bind('<Double-Button-1>', lambda event: self.view_note())

    def refresh_notes(self):
        self.note_listbox.delete(0, tk.END)
        for note in self.notes:
            self.note_listbox.insert(tk.END, note['title'])

    def add_note(self):
        self.open_note_editor()

    def edit_note(self):
        selected_index = self.get_selected_index()
        if selected_index is None:
            messagebox.showwarning("No selection", "Please select a note to edit.")
            return
        note = self.notes[selected_index]
        self.open_note_editor(note, selected_index)

    def delete_note(self):
        selected_index = self.get_selected_index()
        if selected_index is None:
            messagebox.showwarning("No selection", "Please select a note to delete.")
            return
        confirm = messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?")
        if confirm:
            del self.notes[selected_index]
            self.refresh_notes()

    def view_note(self):
        selected_index = self.get_selected_index()
        if selected_index is None:
            return
        note = self.notes[selected_index]
        messagebox.showinfo(note['title'], note['content'])

    def get_selected_index(self):
        try:
            index = self.note_listbox.curselection()[0]
            return index
        except IndexError:
            return None

    def open_note_editor(self, note=None, index=None):
        editor = tk.Toplevel(self.root)
        editor.title("Note Editor")

        tk.Label(editor, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_var = tk.StringVar()
        title_entry = tk.Entry(editor, textvariable=title_var, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(editor, text="Content:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.NW)
        content_text = tk.Text(editor, width=40, height=10)
        content_text.grid(row=1, column=1, padx=5, pady=5)

        if note:
            title_var.set(note['title'])
            content_text.insert(tk.END, note['content'])

        def save():
            title = title_var.get().strip()
            content = content_text.get("1.0", tk.END).strip()
            if not title:
                messagebox.showwarning("Input Error", "Title cannot be empty.")
                return
            if note is None:
                # Adding new note
                self.notes.append({'title': title, 'content': content})
            else:
                # Editing existing note
                self.notes[index] = {'title': title, 'content': content}
            self.refresh_notes()
            editor.destroy()

        save_btn = tk.Button(editor, text="Save", command=save)
        save_btn.grid(row=2, column=1, padx=5, pady=10, sticky=tk.E)

if __name__ == '__main__':
    root = tk.Tk()
    app = NoteTakingApp(root)
    root.mainloop()
