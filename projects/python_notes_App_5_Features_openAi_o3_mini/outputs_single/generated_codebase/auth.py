import tkinter as tk
from tkinter import messagebox
import bcrypt
from database import get_user_by_username, create_user
from encryption_helper import derive_key, generate_salt


class LoginWindow(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.pack(pady=20)

        tk.Label(self, text="Login").pack()

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=5)
        tk.Button(self, text="Register", command=self.open_register).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode('utf-8')
        user = get_user_by_username(username)
        if user and bcrypt.checkpw(password, user['password_hash']):
            # Derive an encryption key based on user's password and stored salt
            encryption_key = derive_key(password, user['encryption_salt'])
            messagebox.showinfo("Success", "Logged in successfully!")
            self.on_success(user, encryption_key)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def open_register(self):
        register_win = tk.Toplevel(self)
        RegisterWindow(register_win)


class RegisterWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(pady=20)

        tk.Label(self, text="Register").pack()

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Register", command=self.register).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode('utf-8')
        if get_user_by_username(username):
            tk.messagebox.showerror("Error", "Username already exists!")
            return
        
        # Generate a salt for encryption and hash password with bcrypt
        encryption_salt = generate_salt()
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        create_user(username, password_hash, encryption_salt)
        tk.messagebox.showinfo("Success", "Registration successful!")
        self.master.destroy()
