import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import json
from database import Database
from config import DEFAULT_EXPORT_PATH

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Note Taking Application')
        self.db = Database()
        self.selected_note_id = None

        # Layout frames
        self.setup_ui()
        self.load_notes()

    def setup_ui(self):
        # Create Menu
        self.create_menu()

        # Create main PanedWindow
        self.paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Left frame: Note List and Search
        self.left_frame = ttk.Frame(self.paned, width=200)
        self.paned.add(self.left_frame, weight=1)

        # Search entry
        self.search_var = tk.StringVar()
        search_frame = ttk.Frame(self.left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text='Search:').pack(side=tk.LEFT)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<KeyRelease>', lambda e: self.search_notes())

        # Note List
        self.note_list = tk.Listbox(self.left_frame)
        self.note_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.note_list.bind('<<ListboxSelect>>', lambda e: self.display_selected_note())

        # Right frame: Note Editor and Preview
        self.right_frame = ttk.Frame(self.paned)
        self.paned.add(self.right_frame, weight=3)

        # Note Title
        title_frame = ttk.Frame(self.right_frame)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(title_frame, text='Title:').pack(side=tk.LEFT)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(title_frame, textvariable=self.title_var)
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Formatting toolbar
        toolbar = ttk.Frame(self.right_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(toolbar, text='Bold', command=self.apply_bold).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text='Italic', command=self.apply_italic).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text='Code', command=self.apply_code).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text='Preview', command=self.update_preview).pack(side=tk.LEFT, padx=2)

        # Notebook for Editor and Preview
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Editor tab
        self.editor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.editor_frame, text='Editor')
        self.editor_text = tk.Text(self.editor_frame, wrap='word', font=('Helvetica', 12))
        self.editor_text.pack(fill=tk.BOTH, expand=True)

        # Preview tab
        self.preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_frame, text='Preview')
        self.preview_text = tk.Text(self.preview_frame, wrap='word', font=('Helvetica', 12), state='disabled')
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Tag configurations for preview
        self.preview_text.tag_configure('bold', font=('Helvetica', 12, 'bold'))
        self.preview_text.tag_configure('italic', font=('Helvetica', 12, 'italic'))
        self.preview_text.tag_configure('code', font=('Courier', 12), background='#f0f0f0')

        # Bottom buttons
        button_frame = ttk.Frame(self.right_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text='New Note', command=self.new_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text='Save', command=self.save_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text='Delete', command=self.delete_note).pack(side=tk.LEFT, padx=2)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Import', command=self.import_notes)
        file_menu.add_command(label='Export', command=self.export_notes)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.quit)

    def load_notes(self):
        self.note_list.delete(0, tk.END)
        self.notes = self.db.get_notes()
        for note in self.notes:
            display_text = f"{note['title']} ({note['updated']})"
            self.note_list.insert(tk.END, display_text)

    def display_selected_note(self):
        selected = self.note_list.curselection()
        if not selected:
            return
        index = selected[0]
        note = self.notes[index]
        self.selected_note_id = note['id']
        self.title_var.set(note['title'])
        self.editor_text.delete('1.0', tk.END)
        self.editor_text.insert(tk.END, note['content'])
        self.update_preview()

    def new_note(self):
        self.selected_note_id = None
        self.title_var.set('')
        self.editor_text.delete('1.0', tk.END)
        self.preview_text.config(state='normal')
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.config(state='disabled')
        self.note_list.selection_clear(0, tk.END)

    def save_note(self):
        title = self.title_var.get().strip()
        content = self.editor_text.get('1.0', tk.END).strip()
        if not title or not content:
            messagebox.showwarning('Validation', 'Title and Content cannot be empty.')
            return
        if self.selected_note_id:
            self.db.update_note(self.selected_note_id, title, content)
        else:
            self.selected_note_id = self.db.add_note(title, content)
        self.load_notes()
        messagebox.showinfo('Success', 'Note saved successfully.')

    def delete_note(self):
        if self.selected_note_id is None:
            messagebox.showwarning('Selection', 'No note selected to delete.')
            return
        if messagebox.askyesno('Confirm Delete', 'Are you sure you want to delete this note?'):
            self.db.delete_note(self.selected_note_id)
            self.new_note()
            self.load_notes()

    def search_notes(self):
        keyword = self.search_var.get().strip()
        if keyword == '':
            self.notes = self.db.get_notes()
        else:
            self.notes = self.db.search_notes(keyword)
        self.note_list.delete(0, tk.END)
        for note in self.notes:
            display_text = f"{note['title']} ({note['updated']})"
            self.note_list.insert(tk.END, display_text)

    def import_notes(self):
        file_path = filedialog.askopenfilename(title='Select JSON file to import', filetypes=[('JSON Files', '*.json')])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = f.read()
                if self.db.import_notes(json_data):
                    messagebox.showinfo('Import', 'Notes imported successfully.')
                    self.load_notes()
                else:
                    messagebox.showerror('Import', 'Failed to import notes.')
            except Exception as e:
                messagebox.showerror('Error', f'Error reading file: {e}')

    def export_notes(self):
        file_path = filedialog.asksaveasfilename(title='Export Notes as JSON', 
                                                 initialdir=DEFAULT_EXPORT_PATH, 
                                                 defaultextension='.json', 
                                                 filetypes=[('JSON Files', '*.json')])
        if file_path:
            try:
                json_data = self.db.export_notes()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(json_data)
                messagebox.showinfo('Export', 'Notes exported successfully.')
            except Exception as e:
                messagebox.showerror('Error', f'Error writing file: {e}')

    # Formatting button functions
    def apply_bold(self):
        self.wrap_selection('**', '**')

    def apply_italic(self):
        self.wrap_selection('*', '*')

    def apply_code(self):
        self.wrap_selection('`', '`')

    def wrap_selection(self, start_tag, end_tag):
        try:
            start = self.editor_text.index('sel.first')
            end = self.editor_text.index('sel.last')
            selected_text = self.editor_text.get(start, end)
            new_text = f'{start_tag}{selected_text}{end_tag}'
            self.editor_text.delete(start, end)
            self.editor_text.insert(start, new_text)
        except tk.TclError:
            messagebox.showwarning('Selection', 'Please select text to format.')

    # Update preview tab with basic markdown rendering
    def update_preview(self):
        content = self.editor_text.get('1.0', tk.END)
        parsed_text, spans = self.parse_markdown(content)
        self.preview_text.config(state='normal')
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', parsed_text)
        # Apply formatting tags
        for span in spans:
            start_idx, end_idx, tag = span
            # Convert indices to Tkinter text indices
            start_index = self.get_text_index_from_pos(parsed_text, start_idx)
            end_index = self.get_text_index_from_pos(parsed_text, end_idx)
            self.preview_text.tag_add(tag, start_index, end_index)
        self.preview_text.config(state='disabled')

    def get_text_index_from_pos(self, text, pos):
        # Given a character position (pos) in text, convert to Tk text index
        # Count number of newlines
        lines = text.split('\n')
        count = 0
        for i, line in enumerate(lines):
            if count + len(line) >= pos:
                col = pos - count
                return f"{i+1}.{col}"
            count += len(line) + 1  # +1 for the newline char
        return tk.END

    def parse_markdown(self, content):
        # A simple parser to remove markdown markers and record formatting spans
        parsed_text = ''
        spans = []  # list of tuples: (start_index, end_index, tag)
        i = 0
        while i < len(content):
            if content[i:i+2] == '**':
                i += 2
                start_pos = len(parsed_text)
                # find closing **
                end_marker = content.find('**', i)
                if end_marker == -1:
                    # no closing marker found, just add the rest
                    parsed_text += '**'
                    break
                inner_text = content[i:end_marker]
                parsed_text += inner_text
                spans.append((start_pos, start_pos + len(inner_text), 'bold'))
                i = end_marker + 2
            elif content[i] == '*' :
                # Avoid matching if it might be part of bold
                if i+1 < len(content) and content[i+1] == '*':
                    # skip because it was handled above
                    i += 1
                    continue
                i += 1
                start_pos = len(parsed_text)
                end_marker = content.find('*', i)
                if end_marker == -1:
                    parsed_text += '*'
                    break
                inner_text = content[i:end_marker]
                parsed_text += inner_text
                spans.append((start_pos, start_pos + len(inner_text), 'italic'))
                i = end_marker + 1
            elif content[i] == '`':
                i += 1
                start_pos = len(parsed_text)
                end_marker = content.find('`', i)
                if end_marker == -1:
                    parsed_text += '`'
                    break
                inner_text = content[i:end_marker]
                parsed_text += inner_text
                spans.append((start_pos, start_pos + len(inner_text), 'code'))
                i = end_marker + 1
            else:
                parsed_text += content[i]
                i += 1
        return parsed_text, spans

if __name__ == '__main__':
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
