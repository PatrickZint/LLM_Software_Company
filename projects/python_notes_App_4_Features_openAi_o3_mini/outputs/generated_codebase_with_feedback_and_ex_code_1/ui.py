import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from database import Database
from import_export import export_notes, import_notes


class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taking Application")
        self.db = Database()
        self.selected_note_id = None
        
        self.create_widgets()
        self.load_notes()

    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame: Search and note list
        self.left_frame = ttk.Frame(self.main_frame, width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self.left_frame, textvariable=self.search_var)
        search_entry.pack(fill=tk.X, padx=5, pady=5)
        search_entry.bind("<KeyRelease>", self.on_search)
        
        self.note_listbox = tk.Listbox(self.left_frame)
        self.note_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.note_listbox.bind("<<ListboxSelect>>", self.on_note_select)
        
        # Buttons for New and Delete
        btn_frame = ttk.Frame(self.left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        self.new_btn = ttk.Button(btn_frame, text="New Note", command=self.new_note)
        self.new_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.delete_btn = ttk.Button(btn_frame, text="Delete Note", command=self.delete_note)
        self.delete_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Right frame: Note details
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(self.right_frame, text="Title:").pack(anchor=tk.W, padx=5, pady=2)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(self.right_frame, textvariable=self.title_var)
        self.title_entry.pack(fill=tk.X, padx=5, pady=2)

        # Categories
        ttk.Label(self.right_frame, text="Categories (comma separated):").pack(anchor=tk.W, padx=5, pady=2)
        self.categories_var = tk.StringVar()
        self.categories_entry = ttk.Entry(self.right_frame, textvariable=self.categories_var)
        self.categories_entry.pack(fill=tk.X, padx=5, pady=2)

        # Tags
        ttk.Label(self.right_frame, text="Tags (comma separated):").pack(anchor=tk.W, padx=5, pady=2)
        self.tags_var = tk.StringVar()
        self.tags_entry = ttk.Entry(self.right_frame, textvariable=self.tags_var)
        self.tags_entry.pack(fill=tk.X, padx=5, pady=2)
        
        # Formatting toolbar for Rich Text & Markdown support
        self.format_toolbar = ttk.Frame(self.right_frame)
        self.format_toolbar.pack(fill=tk.X, padx=5, pady=2)
        
        bold_btn = ttk.Button(self.format_toolbar, text="Bold", command=self.apply_bold)
        bold_btn.pack(side=tk.LEFT, padx=2)
        italic_btn = ttk.Button(self.format_toolbar, text="Italic", command=self.apply_italic)
        italic_btn.pack(side=tk.LEFT, padx=2)
        code_btn = ttk.Button(self.format_toolbar, text="Code Snippet", command=self.apply_code)
        code_btn.pack(side=tk.LEFT, padx=2)

        # Content (supports Markdown formatting and rich text editing via toolbar)
        ttk.Label(self.right_frame, text="Content (Markdown Supported):").pack(anchor=tk.W, padx=5, pady=2)
        self.content_text = tk.Text(self.right_frame, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Save button
        self.save_btn = ttk.Button(self.right_frame, text="Save Note", command=self.save_note)
        self.save_btn.pack(padx=5, pady=5)

        # Menu for Export/Import
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Export Notes", command=self.export_notes)
        filemenu.add_command(label="Import Notes", command=self.import_notes)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def apply_format(self, prefix, suffix):
        try:
            start_index = self.content_text.index("sel.first")
            end_index = self.content_text.index("sel.last")
            selected_text = self.content_text.get(start_index, end_index)
            formatted_text = f"{prefix}{selected_text}{suffix}"
            self.content_text.delete(start_index, end_index)
            self.content_text.insert(start_index, formatted_text)
        except tk.TclError:
            messagebox.showwarning("Selection Error", "Please select text to format.")

    def apply_bold(self):
        # Wraps the selected text in ** for Markdown bold formatting
        self.apply_format("**", "**")

    def apply_italic(self):
        # Wraps the selected text in * for Markdown italic formatting
        self.apply_format("*", "*")

    def apply_code(self):
        # Optionally, allow the user to specify a programming language via an input dialog
        language = simpledialog.askstring("Code Snippet", "Enter language (optional):")
        prefix = "```" + (language.strip() if language else "") + "\n"
        suffix = "\n```"
        self.apply_format(prefix, suffix)

    def load_notes(self):
        self.note_listbox.delete(0, tk.END)
        self.notes = self.db.get_all_notes()
        for note in self.notes:
            display_text = f"{note['title']} - {note['created_at'][:10]}"
            self.note_listbox.insert(tk.END, display_text)

    def on_note_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            self.selected_note_id = note['id']
            self.title_var.set(note['title'])
            self.categories_var.set(", ".join(note.get('categories', [])))
            self.tags_var.set(", ".join(note.get('tags', [])))
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, note['content'])
        else:
            self.selected_note_id = None

    def new_note(self):
        self.selected_note_id = None
        self.title_var.set("")
        self.categories_var.set("")
        self.tags_var.set("")
        self.content_text.delete("1.0", tk.END)
        self.note_listbox.selection_clear(0, tk.END)

    def save_note(self):
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        categories = [cat.strip() for cat in self.categories_var.get().split(",") if cat.strip()]
        tags = [tag.strip() for tag in self.tags_var.get().split(",") if tag.strip()]

        if not title or not content:
            messagebox.showwarning("Incomplete Data", "Title and Content are required.")
            return

        if self.selected_note_id:
            self.db.update_note(self.selected_note_id, title, content, categories, tags)
            messagebox.showinfo("Note Updated", "The note has been updated successfully.")
        else:
            self.db.create_note(title, content, categories, tags)
            messagebox.showinfo("Note Created", "The note has been created successfully.")
        self.load_notes()

    def delete_note(self):
        if self.selected_note_id:
            answer = messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?")
            if answer:
                self.db.delete_note(self.selected_note_id)
                self.new_note()
                self.load_notes()
        else:
            messagebox.showwarning("No Selection", "No note selected to delete.")

    def on_search(self, event):
        keyword = self.search_var.get().strip()
        if keyword:
            self.notes = self.db.search_notes(keyword)
        else:
            self.notes = self.db.get_all_notes()
        self.note_listbox.delete(0, tk.END)
        for note in self.notes:
            display_text = f"{note['title']} - {note['created_at'][:10]}"
            self.note_listbox.insert(tk.END, display_text)

    def export_notes(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            export_notes(self.db, file_path)
            messagebox.showinfo("Export Successful", f"Notes exported to {file_path}")

    def import_notes(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            import_notes(self.db, file_path)
            self.load_notes()
            messagebox.showinfo("Import Successful", f"Notes imported from {file_path}")
