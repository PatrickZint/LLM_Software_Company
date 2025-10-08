import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk
from note_model import Note
import json
import os

# For Markdown rendering, we use the markdown module to convert markdown to HTML
# and tkhtmlview to display the HTML content.
# Make sure to install these with: pip install markdown tkhtmlview
import markdown
from tkhtmlview import HTMLLabel


class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Note Taking Application')
        self.geometry('900x600')

        self.create_menu()
        self.create_widgets()
        self.refresh_notes()

    def create_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='New Note', command=self.new_note)
        file_menu.add_command(label='Import Notes', command=self.import_notes)
        file_menu.add_command(label='Export Notes', command=self.export_notes)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.quit)
        menubar.add_cascade(label='File', menu=file_menu)
        self.config(menu=menubar)

    def create_widgets(self):
        # Pane for list and details
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left frame: list of notes and search
        self.left_frame = ttk.Frame(self.paned_window, width=250)
        self.paned_window.add(self.left_frame, weight=1)

        # Right frame: note details and editor
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, weight=3)

        # Search bar
        search_frame = ttk.Frame(self.left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind('<Return>', lambda event: self.search_notes())
        ttk.Button(search_frame, text='Search', command=self.search_notes).pack(side=tk.LEFT, padx=2)

        # Listbox for notes
        self.listbox = tk.Listbox(self.left_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', lambda event: self.on_note_select())

        # Note detail frame (title and content editor)
        detail_frame = ttk.Frame(self.right_frame)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(detail_frame, text='Title:').pack(anchor=tk.W)
        self.title_entry = ttk.Entry(detail_frame)
        self.title_entry.pack(fill=tk.X, pady=2)

        ttk.Label(detail_frame, text='Content:').pack(anchor=tk.W)
        self.content_text = tk.Text(detail_frame, wrap='word', height=20)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=2)

        # Metadata fields (categories and tags)
        meta_frame = ttk.Frame(detail_frame)
        meta_frame.pack(fill=tk.X, pady=5)

        ttk.Label(meta_frame, text='Categories:').grid(row=0, column=0, sticky=tk.W)
        self.categories_entry = ttk.Entry(meta_frame)
        self.categories_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)

        ttk.Label(meta_frame, text='Tags:').grid(row=1, column=0, sticky=tk.W)
        self.tags_entry = ttk.Entry(meta_frame)
        self.tags_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        meta_frame.columnconfigure(1, weight=1)

        # Buttons for operations
        btn_frame = ttk.Frame(detail_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text='Save', command=self.save_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='Delete', command=self.delete_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text='Preview Markdown', command=self.preview_markdown).pack(side=tk.LEFT, padx=5)

        # Currently selected note id
        self.current_note_id = None

    def refresh_notes(self):
        self.listbox.delete(0, tk.END)
        self.notes = Note.get_all()
        for note in self.notes:
            display_text = f"{note.title} - {note.created}"
            self.listbox.insert(tk.END, display_text)

    def clear_note_fields(self):
        self.current_note_id = None
        self.title_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.categories_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)

    def on_note_select(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            self.current_note_id = note.id
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note.title)
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, note.content)
            self.categories_entry.delete(0, tk.END)
            self.categories_entry.insert(0, note.categories or '')
            self.tags_entry.delete(0, tk.END)
            self.tags_entry.insert(0, note.tags or '')

    def new_note(self):
        self.clear_note_fields()
        self.listbox.selection_clear(0, tk.END)

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        categories = self.categories_entry.get().strip()
        tags = self.tags_entry.get().strip()

        if not title or not content:
            messagebox.showwarning('Input Error', 'Title and Content cannot be empty.')
            return

        if self.current_note_id:
            Note.update(self.current_note_id, title, content, categories, tags)
            messagebox.showinfo('Success', 'Note updated successfully.')
        else:
            Note.create(title, content, categories, tags)
            messagebox.showinfo('Success', 'Note created successfully.')

        self.refresh_notes()
        self.clear_note_fields()

    def delete_note(self):
        if not self.current_note_id:
            messagebox.showwarning('Selection Error', 'Please select a note to delete.')
            return
        confirm = messagebox.askyesno('Confirm Delete', 'Are you sure you want to delete this note?')
        if confirm:
            Note.delete(self.current_note_id)
            messagebox.showinfo('Deleted', 'Note deleted successfully.')
            self.refresh_notes()
            self.clear_note_fields()

    def search_notes(self):
        keyword = self.search_entry.get().strip()
        if keyword:
            self.notes = Note.search(keyword)
        else:
            self.notes = Note.get_all()
        self.listbox.delete(0, tk.END)
        for note in self.notes:
            display_text = f"{note.title} - {note.created}"
            self.listbox.insert(tk.END, display_text)

    def import_notes(self):
        file_path = filedialog.askopenfilename(title='Select JSON File', filetypes=[('JSON files', '*.json')])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # Expecting a list of note dictionaries
                    for note_data in data:
                        title = note_data.get('title', '')
                        content = note_data.get('content', '')
                        categories = note_data.get('categories', '')
                        tags = note_data.get('tags', '')
                        # Insert note (you may want to add merging logic here)
                        Note.create(title, content, categories, tags)
                messagebox.showinfo('Import', 'Notes imported successfully.')
                self.refresh_notes()
            except Exception as e:
                messagebox.showerror('Error', f'Failed to import notes: {e}')

    def export_notes(self):
        export_path = filedialog.asksaveasfilename(defaultextension='.json', title='Export Notes', filetypes=[('JSON files', '*.json')])
        if export_path:
            try:
                notes = Note.get_all()
                data = []
                for note in notes:
                    data.append({
                        'id': note.id,
                        'title': note.title,
                        'content': note.content,
                        'created': note.created,
                        'updated': note.updated,
                        'categories': note.categories,
                        'tags': note.tags
                    })
                with open(export_path, 'w') as f:
                    json.dump(data, f, indent=4)
                messagebox.showinfo('Export', 'Notes exported successfully.')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to export notes: {e}')

    def preview_markdown(self):
        content = self.content_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning('No Content', 'There is no content to preview.')
            return
        html_content = markdown.markdown(content)
        # Create a new Toplevel window for preview
        preview_win = tk.Toplevel(self)
        preview_win.title('Markdown Preview')
        preview_win.geometry('600x400')

        # Using HTMLLabel from tkhtmlview to render the HTML content
        html_label = HTMLLabel(preview_win, html=html_content)
        html_label.pack(fill='both', expand=True, padx=10, pady=10)


if __name__ == '__main__':
    app = NoteApp()
    app.mainloop()
