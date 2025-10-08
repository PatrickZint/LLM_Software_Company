import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import db
import utils


class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Note Taking App')
        self.geometry('800x600')
        
        # Initialize the database
        db.init_db()
        
        # Initialize selected note id
        self.selected_note_id = None
        
        # Create UI components
        self.create_widgets()
        self.refresh_notes()

    def create_widgets(self):
        # Top frame for Search and Export/Import
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(top_frame, text='Search:').pack(side=tk.LEFT)
        self.search_entry = tk.Entry(top_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(top_frame, text='Search', command=self.search_notes)
        search_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(top_frame, text='Reset', command=self.refresh_notes)
        reset_btn.pack(side=tk.LEFT, padx=5)

        import_btn = tk.Button(top_frame, text='Import', command=self.import_notes)
        import_btn.pack(side=tk.RIGHT, padx=5)
        
        export_btn = tk.Button(top_frame, text='Export', command=self.export_notes)
        export_btn.pack(side=tk.RIGHT, padx=5)

        # Main frame splitter: Left for note list, right for note details
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left frame - Treeview for notes
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.tree = ttk.Treeview(left_frame, columns=('Title', 'Timestamp'), show='headings')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Timestamp', text='Timestamp')
        self.tree.bind('<<TreeviewSelect>>', self.on_note_select)
        self.tree.pack(side=tk.LEFT, fill=tk.Y)

        scrollbar = ttk.Scrollbar(left_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Right frame - Note form
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(right_frame, text='Title').grid(row=0, column=0, sticky=tk.W, pady=2)
        self.title_entry = tk.Entry(right_frame)
        self.title_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)

        tk.Label(right_frame, text='Content').grid(row=1, column=0, sticky=tk.NW, pady=2)
        self.content_text = tk.Text(right_frame, height=10)
        self.content_text.grid(row=1, column=1, sticky=tk.EW, pady=2)

        tk.Label(right_frame, text='Category').grid(row=2, column=0, sticky=tk.W, pady=2)
        self.category_entry = tk.Entry(right_frame)
        self.category_entry.grid(row=2, column=1, sticky=tk.EW, pady=2)

        tk.Label(right_frame, text='Tags (comma separated)').grid(row=3, column=0, sticky=tk.W, pady=2)
        self.tags_entry = tk.Entry(right_frame)
        self.tags_entry.grid(row=3, column=1, sticky=tk.EW, pady=2)

        # Buttons Frame
        btn_frame = tk.Frame(right_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        add_btn = tk.Button(btn_frame, text='Add Note', command=self.add_note)
        add_btn.pack(side=tk.LEFT, padx=5)

        update_btn = tk.Button(btn_frame, text='Update Note', command=self.update_note)
        update_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(btn_frame, text='Delete Note', command=self.delete_note)
        delete_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(btn_frame, text='Clear', command=self.clear_form)
        clear_btn.pack(side=tk.LEFT, padx=5)

        right_frame.columnconfigure(1, weight=1)

    def refresh_notes(self):
        # Clear current tree view
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        notes = db.get_all_notes()
        for note in notes:
            self.tree.insert('', 'end', iid=note['id'], values=(note['title'], note['timestamp']))

    def on_note_select(self, event):
        selected = self.tree.selection()
        if selected:
            note_id = selected[0]
            notes = db.get_all_notes()
            for note in notes:
                if str(note['id']) == note_id:
                    self.title_entry.delete(0, tk.END)
                    self.title_entry.insert(0, note['title'])

                    self.content_text.delete('1.0', tk.END)
                    self.content_text.insert(tk.END, note['content'])

                    self.category_entry.delete(0, tk.END)
                    self.category_entry.insert(0, note['category'] if note['category'] else '')

                    self.tags_entry.delete(0, tk.END)
                    self.tags_entry.insert(0, note['tags'] if note['tags'] else '')

                    self.selected_note_id = note['id']
                    break

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete('1.0', tk.END)
        self.category_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)
        self.selected_note_id = None
        self.tree.selection_remove(self.tree.selection())

    def add_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()
        category = self.category_entry.get().strip()
        tags = self.tags_entry.get().strip()
        
        if not title or not content:
            messagebox.showwarning('Validation Error', 'Title and Content are required.')
            return

        db.add_note(title, content, category, tags)
        self.refresh_notes()
        self.clear_form()

    def update_note(self):
        if not self.selected_note_id:
            messagebox.showwarning('Selection Error', 'Please select a note to update.')
            return

        title = self.title_entry.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()
        category = self.category_entry.get().strip()
        tags = self.tags_entry.get().strip()
        
        if not title or not content:
            messagebox.showwarning('Validation Error', 'Title and Content are required.')
            return

        db.update_note(self.selected_note_id, title, content, category, tags)
        self.refresh_notes()
        self.clear_form()

    def delete_note(self):
        if not self.selected_note_id:
            messagebox.showwarning('Selection Error', 'Please select a note to delete.')
            return

        if messagebox.askyesno('Confirm Delete', 'Are you sure you want to delete this note?'):
            db.delete_note(self.selected_note_id)
            self.refresh_notes()
            self.clear_form()

    def search_notes(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.refresh_notes()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        notes = db.search_notes(keyword)
        for note in notes:
            self.tree.insert('', 'end', iid=note['id'], values=(note['title'], note['timestamp']))

    def export_notes(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON Files', '*.json')])
        if file_path:
            utils.export_notes_to_json(file_path)
            messagebox.showinfo('Export Successful', f'Notes exported to {file_path}')

    def import_notes(self):
        file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
        if file_path:
            utils.import_notes_from_json(file_path)
            self.refresh_notes()
            messagebox.showinfo('Import Successful', f'Notes imported from {file_path}')


if __name__ == '__main__':
    app = NoteApp()
    app.mainloop()
