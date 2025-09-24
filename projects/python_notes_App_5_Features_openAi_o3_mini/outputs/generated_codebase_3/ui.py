'''UI module: Defines Tkinter-based user interface for login/registration and note management'''

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import datetime
from database import get_user, add_user, add_note, get_notes, update_note, delete_note
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
        self.create_widgets()
        self.refresh_notes()

    def create_widgets(self):
        # List of notes
        self.note_list = tk.Listbox(self, height=10)
        self.note_list.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.note_list.bind('<<ListboxSelect>>', self.on_note_select)

        ttk.Button(self, text="New Note", command=self.new_note).grid(row=1, column=0, pady=5)
        ttk.Button(self, text="Delete Note", command=self.delete_selected_note).grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Title:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.title_entry = ttk.Entry(self)
        self.title_entry.grid(row=2, column=1, sticky="ew", pady=(10, 0))

        ttk.Label(self, text="Content:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.content_text = scrolledtext.ScrolledText(self, wrap='word', height=10)
        self.content_text.grid(row=3, column=1, sticky="nsew", pady=(10, 0))

        ttk.Button(self, text="Save Note", command=self.save_note).grid(row=4, column=0, columnspan=2, pady=10)

        self.rowconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)

    def refresh_notes(self):
        self.note_list.delete(0, tk.END)
        notes = get_notes(self.user["id"])
        self.notes = []
        for note in notes:
            self.notes.append(note)
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
