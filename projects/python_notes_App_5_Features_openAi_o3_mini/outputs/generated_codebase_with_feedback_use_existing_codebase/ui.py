'''UI module: Defines Tkinter-based user interface for login/registration and note management
with enhanced features such as note search, JSON export/import, markdown preview, and simple text formatting.''' 

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext, filedialog
import datetime
import json

# Optional markdown support
try:
    import markdown
except ImportError:
    markdown = None

from database import get_user, add_user, add_note, get_notes, update_note, delete_note, search_notes
from security import hash_password, verify_password, derive_key, encrypt_note_content, decrypt_note_content


class LoginFrame(ttk.Frame):
    def __init__(self, master, on_login, on_register):
        super().__init__(master)
        self.on_login = on_login
        self.on_register = on_register
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Username:").grid(row=0, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self, textvariable=self.username_var).grid(row=0, column=1, pady=5)
        ttk.Label(self, text="Password:").grid(row=1, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=5)
        
        ttk.Button(self, text="Login", command=self.login).grid(row=2, column=0, pady=5)
        ttk.Button(self, text="Register", command=self.register).grid(row=2, column=1, pady=5)

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        user_data = get_user(username)
        if user_data and verify_password(password, user_data["password_hash"]):
            # Derive the encryption key from the password and stored salt
            key = derive_key(password, user_data["salt"])
            self.on_login(user_data, key)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        self.on_register()


class NoteFrame(ttk.Frame):
    def __init__(self, master, user, encryption_key):
        super().__init__(master)
        self.user = user
        self.encryption_key = encryption_key
        self.selected_note_id = None
        self.notes = []
        self.create_widgets()
        self.refresh_notes()

    def create_widgets(self):
        # Control Frame for search, export, import, preview, and formatting buttons
        control_frame = ttk.Frame(self)
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)

        # Search functionality
        ttk.Label(control_frame, text="Search:").grid(row=0, column=0, padx=2)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=1, padx=2)
        ttk.Button(control_frame, text="Search", command=self.search_notes).grid(row=0, column=2, padx=2)

        # Export and Import buttons
        ttk.Button(control_frame, text="Export Notes", command=self.export_notes).grid(row=0, column=3, padx=2)
        ttk.Button(control_frame, text="Import Notes", command=self.import_notes).grid(row=0, column=4, padx=2)

        # Markdown preview button
        ttk.Button(control_frame, text="Preview Markdown", command=self.preview_markdown).grid(row=0, column=5, padx=2)

        # Formatting buttons
        ttk.Button(control_frame, text="Bold", command=self.apply_bold).grid(row=0, column=6, padx=2)
        ttk.Button(control_frame, text="Italic", command=self.apply_italic).grid(row=0, column=7, padx=2)
        ttk.Button(control_frame, text="Header", command=self.apply_header).grid(row=0, column=8, padx=2)

        # List of notes
        self.note_list = tk.Listbox(self, height=10)
        self.note_list.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5)
        self.note_list.bind('<<ListboxSelect>>', self.on_note_select)

        # New and Delete buttons
        ttk.Button(self, text="New Note", command=self.new_note).grid(row=2, column=0, pady=5)
        ttk.Button(self, text="Delete Note", command=self.delete_selected_note).grid(row=2, column=1, pady=5)

        # Title and Content Fields
        ttk.Label(self, text="Title:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0), padx=5)
        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(row=3, column=1, sticky="ew", pady=(10, 0), padx=5)

        ttk.Label(self, text="Content:").grid(row=4, column=0, sticky=tk.W, pady=(10, 0), padx=5)
        self.content_text = scrolledtext.ScrolledText(self, wrap='word', height=10)
        self.content_text.grid(row=4, column=1, sticky="nsew", pady=(10, 0), padx=5)

        ttk.Button(self, text="Save Note", command=self.save_note).grid(row=5, column=0, columnspan=2, pady=10)

        self.rowconfigure(4, weight=1)
        self.columnconfigure(1, weight=1)

    def refresh_notes(self, notes_data=None):
        self.note_list.delete(0, tk.END)
        if notes_data is None:
            notes_data = get_notes(self.user["id"])
        self.notes = notes_data
        for note in self.notes:
            display_text = f"{note['title']} - {note['timestamp']}"
            self.note_list.insert(tk.END, display_text)

    def on_note_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            self.selected_note_id = note["id"]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note["title"])
            try:
                decrypted = decrypt_note_content(note["content"], self.encryption_key)
            except Exception as e:
                decrypted = "Error decrypting note"
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, decrypted)

    def new_note(self):
        self.selected_note_id = None
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.note_list.selection_clear(0, tk.END)

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showerror("Error", "Title and content cannot be empty")
            return
        encrypted_content = encrypt_note_content(content, self.encryption_key)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.selected_note_id:
            update_note(self.selected_note_id, title, encrypted_content)
        else:
            add_note(self.user["id"], title, encrypted_content, timestamp)
        self.refresh_notes()

    def delete_selected_note(self):
        selection = self.note_list.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
                delete_note(note["id"])
                self.new_note()
                self.refresh_notes()

    def search_notes(self):
        query = self.search_var.get().strip()
        if query:
            results = search_notes(self.user["id"], query)
            self.refresh_notes(notes_data=results)
        else:
            self.refresh_notes()

    def export_notes(self):
        notes = get_notes(self.user["id"])
        export_list = []
        for note in notes:
            try:
                content = decrypt_note_content(note["content"], self.encryption_key)
            except Exception:
                content = "<Decryption Error>"
            export_list.append({
                "title": note["title"],
                "content": content,
                "timestamp": note["timestamp"],
                "tags": note["tags"],
                "categories": note["categories"]
            })
        file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON Files', '*.json')])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_list, f, indent=4)
                messagebox.showinfo("Export", "Notes exported successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting notes: {e}")

    def import_notes(self):
        file_path = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_notes = json.load(f)
                # Validate and import each note
                for note in imported_notes:
                    if 'title' in note and 'content' in note and 'timestamp' in note:
                        # Encrypt the content before storing
                        encrypted_content = encrypt_note_content(note['content'], self.encryption_key)
                        add_note(self.user["id"], note['title'], encrypted_content, note['timestamp'], note.get('tags'), note.get('categories'))
                    else:
                        messagebox.showwarning("Import Warning", "One or more notes have an invalid format and were skipped.")
                messagebox.showinfo("Import", "Notes imported successfully.")
                self.refresh_notes()
            except Exception as e:
                messagebox.showerror("Import Error", f"Error importing notes: {e}")

    def preview_markdown(self):
        content = self.content_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("Preview", "No content to preview.")
            return
        if markdown is None:
            messagebox.showerror("Markdown Error", "The markdown module is not installed.")
            return
        html = markdown.markdown(content)

        preview_win = tk.Toplevel(self)
        preview_win.title("Markdown Preview")
        preview_text = scrolledtext.ScrolledText(preview_win, wrap='word', width=80, height=30)
        preview_text.pack(fill='both', expand=True)
        preview_text.insert(tk.END, html)
        preview_text.config(state=tk.DISABLED)

    def apply_bold(self):
        try:
            start = self.content_text.index(tk.SEL_FIRST)
            end = self.content_text.index(tk.SEL_LAST)
            selected_text = self.content_text.get(start, end)
            new_text = f"**{selected_text}**"
            self.content_text.delete(start, end)
            self.content_text.insert(start, new_text)
        except tk.TclError:
            messagebox.showinfo("Formatting", "No text selected")

    def apply_italic(self):
        try:
            start = self.content_text.index(tk.SEL_FIRST)
            end = self.content_text.index(tk.SEL_LAST)
            selected_text = self.content_text.get(start, end)
            new_text = f"*{selected_text}*"
            self.content_text.delete(start, end)
            self.content_text.insert(start, new_text)
        except tk.TclError:
            messagebox.showinfo("Formatting", "No text selected")

    def apply_header(self):
        try:
            # Get the index of the start of the current line
            index = self.content_text.index(tk.INSERT + " linestart")
            self.content_text.insert(index, "# ")
        except Exception as e:
            messagebox.showerror("Formatting Error", str(e))


def registration_dialog(master):
    reg_win = tk.Toplevel(master)
    reg_win.title("Register New User")
    
    ttk.Label(reg_win, text="Username:").grid(row=0, column=0, pady=5, sticky=tk.W)
    username_entry = ttk.Entry(reg_win)
    username_entry.grid(row=0, column=1, pady=5)
    
    ttk.Label(reg_win, text="Password:").grid(row=1, column=0, pady=5, sticky=tk.W)
    password_entry = ttk.Entry(reg_win, show="*")
    password_entry.grid(row=1, column=1, pady=5)

    def register_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        if get_user(username):
            messagebox.showerror("Error", "Username already exists")
            return
        pwd_hash, salt = hash_password(password)
        add_user(username, pwd_hash, salt)
        messagebox.showinfo("Success", "User registered successfully")
        reg_win.destroy()

    ttk.Button(reg_win, text="Register", command=register_user).grid(row=2, column=0, columnspan=2, pady=10)
