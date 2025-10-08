import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font

from note_controller import NoteController
from config_manager import ConfigManager
from formatting_controller import FormattingController


class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.controller = NoteController()
        self.config_manager = ConfigManager()
        self.formatting_controller = FormattingController()
        self.current_format_mode = "WYSIWYG"  # Modes: WYSIWYG or Markdown
        self.current_note_id = None
        self.notes = []
        self.create_widgets()
        self.load_notes()

    def create_widgets(self):
        # Header Frame for navigation buttons
        self.header_frame = tk.Frame(self, height=50, bg='lightgray')
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_create = tk.Button(self.header_frame, text='Create Note', command=self.create_note)
        self.btn_create.pack(side=tk.LEFT, padx=5, pady=10)
        self.btn_export = tk.Button(self.header_frame, text='Export', command=self.export_notes)
        self.btn_export.pack(side=tk.LEFT, padx=5, pady=10)
        self.btn_import = tk.Button(self.header_frame, text='Import', command=self.import_notes)
        self.btn_import.pack(side=tk.LEFT, padx=5, pady=10)

        # Sidebar Frame for filters (e.g., search, categories, tags)
        self.sidebar_frame = tk.Frame(self, width=200, bg='white')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Search field in sidebar
        self.lbl_search = tk.Label(self.sidebar_frame, text='Search', bg='white')
        self.lbl_search.pack(padx=10, pady=(10,0))
        self.ent_search = tk.Entry(self.sidebar_frame)
        self.ent_search.pack(padx=10, pady=5, fill=tk.X)
        self.btn_search = tk.Button(self.sidebar_frame, text='Search', command=self.do_search)
        self.btn_search.pack(padx=10, pady=5)
        self.btn_clear_search = tk.Button(self.sidebar_frame, text='Clear', command=self.load_notes)
        self.btn_clear_search.pack(padx=10, pady=5)

        # Main Frame for list view and detailed editor
        self.main_frame = tk.Frame(self, bg='white')
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # List of notes
        self.list_frame = tk.Frame(self.main_frame, bg='white')
        self.list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.note_list = tk.Listbox(self.list_frame, width=30)
        self.note_list.pack(side=tk.TOP, fill=tk.Y, expand=True)
        self.note_list.bind('<<ListboxSelect>>', self.on_note_select)

        # Editor Panel
        self.editor_frame = tk.Frame(self.main_frame, bg='white')
        self.editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Fields for Title, Categories and Tags
        self.meta_frame = tk.Frame(self.editor_frame, bg='white')
        self.meta_frame.pack(side=tk.TOP, fill=tk.X, pady=(0,5))

        tk.Label(self.meta_frame, text='Title:').grid(row=0, column=0, padx=2, pady=2, sticky='e')
        self.ent_title = tk.Entry(self.meta_frame)
        self.ent_title.grid(row=0, column=1, padx=2, pady=2, sticky='we')

        tk.Label(self.meta_frame, text='Categories (comma separated):').grid(row=1, column=0, padx=2, pady=2, sticky='e')
        self.ent_categories = tk.Entry(self.meta_frame)
        self.ent_categories.grid(row=1, column=1, padx=2, pady=2, sticky='we')

        tk.Label(self.meta_frame, text='Tags (comma separated):').grid(row=2, column=0, padx=2, pady=2, sticky='e')
        self.ent_tags = tk.Entry(self.meta_frame)
        self.ent_tags.grid(row=2, column=1, padx=2, pady=2, sticky='we')

        self.meta_frame.columnconfigure(1, weight=1)

        # Formatting toolbar above the text editor
        self.formatting_frame = tk.Frame(self.editor_frame, bg='lightblue')
        self.formatting_frame.pack(side=tk.TOP, fill=tk.X)
        self.btn_bold = tk.Button(self.formatting_frame, text="Bold", command=lambda: self.apply_format("bold"))
        self.btn_bold.pack(side=tk.LEFT, padx=2, pady=2)
        self.btn_italic = tk.Button(self.formatting_frame, text="Italic", command=lambda: self.apply_format("italic"))
        self.btn_italic.pack(side=tk.LEFT, padx=2, pady=2)
        self.btn_underline = tk.Button(self.formatting_frame, text="Underline", command=lambda: self.apply_format("underline"))
        self.btn_underline.pack(side=tk.LEFT, padx=2, pady=2)
        self.btn_code = tk.Button(self.formatting_frame, text="Code", command=lambda: self.apply_format("code"))
        self.btn_code.pack(side=tk.LEFT, padx=2, pady=2)
        self.btn_toggle_mode = tk.Button(self.formatting_frame, text="Toggle to Markdown", command=self.toggle_format_mode)
        self.btn_toggle_mode.pack(side=tk.LEFT, padx=2, pady=2)

        # Text editor
        self.txt_editor = tk.Text(self.editor_frame, wrap=tk.WORD)
        self.txt_editor.pack(fill=tk.BOTH, expand=True)

        # Setup text tags for WYSIWYG formatting
        bold_font = font.Font(self.txt_editor, self.txt_editor.cget("font"))
        bold_font.configure(weight="bold")
        self.txt_editor.tag_configure("bold", font=bold_font)

        italic_font = font.Font(self.txt_editor, self.txt_editor.cget("font"))
        italic_font.configure(slant="italic")
        self.txt_editor.tag_configure("italic", font=italic_font)

        underline_font = font.Font(self.txt_editor, self.txt_editor.cget("font"))
        underline_font.configure(underline=True)
        self.txt_editor.tag_configure("underline", font=underline_font)

        code_font = font.Font(family="Courier", size=10)
        self.txt_editor.tag_configure("code", font=code_font, background="#f0f0f0")

        # Save and Delete buttons
        self.action_frame = tk.Frame(self.editor_frame, bg='white')
        self.action_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        self.btn_save = tk.Button(self.action_frame, text='Save', command=self.save_note)
        self.btn_save.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_delete = tk.Button(self.action_frame, text='Delete', command=self.delete_note)
        self.btn_delete.pack(side=tk.LEFT, padx=5, pady=5)

    def apply_format(self, tag):
        try:
            # Get selection range
            start = self.txt_editor.index("sel.first")
            end = self.txt_editor.index("sel.last")
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select text to format")
            return

        if self.current_format_mode == "WYSIWYG":
            # Toggle the formatting tag on the selected text
            if tag in self.txt_editor.tag_names("sel.first"):
                self.txt_editor.tag_remove(tag, start, end)
            else:
                self.txt_editor.tag_add(tag, start, end)
        else:
            # In Markdown mode, wrap the selection with corresponding markdown symbols
            content = self.txt_editor.get(start, end)
            md_wrappers = {
                "bold": "**",
                "italic": "*",
                "underline": "__",
                "code": "`
            }
            wrapper = md_wrappers.get(tag, "")
            new_content = wrapper + content + wrapper
            self.txt_editor.delete(start, end)
            self.txt_editor.insert(start, new_content)

    def toggle_format_mode(self):
        if self.current_format_mode == "WYSIWYG":
            # Convert current text to markdown using formatting_controller (stub implementation)
            content = self.txt_editor.get("1.0", tk.END)
            new_content = self.formatting_controller.toggle_formatting(content, mode="markdown")
            self.txt_editor.delete("1.0", tk.END)
            self.txt_editor.insert("1.0", new_content)
            self.current_format_mode = "Markdown"
            self.btn_toggle_mode.config(text="Toggle to WYSIWYG")
        else:
            content = self.txt_editor.get("1.0", tk.END)
            new_content = self.formatting_controller.toggle_formatting(content, mode="wysiwyg")
            self.txt_editor.delete("1.0", tk.END)
            self.txt_editor.insert("1.0", new_content)
            self.current_format_mode = "WYSIWYG"
            self.btn_toggle_mode.config(text="Toggle to Markdown")

    def load_notes(self):
        self.note_list.delete(0, tk.END)
        self.notes = self.controller.get_all_notes()
        for note in self.notes:
            # Display id and title
            self.note_list.insert(tk.END, f"{note['id']}: {note['title']}")
        # Clear editor fields
        self.clear_editor()

    def clear_editor(self):
        self.current_note_id = None
        self.ent_title.delete(0, tk.END)
        self.ent_categories.delete(0, tk.END)
        self.ent_tags.delete(0, tk.END)
        self.txt_editor.delete('1.0', tk.END)

    def on_note_select(self, event):
        selection = self.note_list.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            self.current_note_id = note['id']
            self.ent_title.delete(0, tk.END)
            self.ent_title.insert(0, note['title'])
            self.ent_categories.delete(0, tk.END)
            self.ent_categories.insert(0, ', '.join(note.get('categories', [])))
            self.ent_tags.delete(0, tk.END)
            self.ent_tags.insert(0, ', '.join(note.get('tags', [])))
            self.txt_editor.delete('1.0', tk.END)
            self.txt_editor.insert(tk.END, note['content'])
        else:
            self.current_note_id = None

    def create_note(self):
        # Create a new note with default metadata
        title = 'New Note'
        content = ''
        note_id = self.controller.create_note(title, content, categories=[], tags=[])
        self.load_notes()
        messagebox.showinfo('Info', 'Note created successfully')

    def save_note(self):
        if self.current_note_id:
            title = self.ent_title.get()
            content = self.txt_editor.get('1.0', tk.END)
            # Get categories and tags as lists (split by comma and strip spaces)
            categories = [c.strip() for c in self.ent_categories.get().split(",") if c.strip()]
            tags = [t.strip() for t in self.ent_tags.get().split(",") if t.strip()]
            self.controller.update_note(self.current_note_id, title=title, content=content, categories=categories, tags=tags)
            self.load_notes()
            messagebox.showinfo('Info', 'Note updated successfully')
        else:
            messagebox.showwarning('Warning', 'No note selected')

    def delete_note(self):
        if self.current_note_id:
            if messagebox.askyesno('Confirm', 'Are you sure you want to delete this note?'):
                self.controller.delete_note(self.current_note_id)
                self.load_notes()
                self.clear_editor()
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

    def do_search(self):
        keyword = self.ent_search.get().strip()
        if keyword:
            self.notes = self.controller.search_notes(keyword)
            self.note_list.delete(0, tk.END)
            for note in self.notes:
                self.note_list.insert(tk.END, f"{note['id']}: {note['title']}")
        else:
            self.load_notes()
