'''Main module: Application entry point for the Secure Note-Taking Application'''

import tkinter as tk
from tkinter import ttk
from database import init_db
from ui import LoginFrame, NoteFrame, registration_dialog


def on_login(user, encryption_key):
    login_frame.destroy()
    note_frame = NoteFrame(root, user, encryption_key)
    note_frame.pack(fill="both", expand=True)


def on_register():
    registration_dialog(root)


if __name__ == "__main__":
    # Initialize the local SQLite database
    init_db()

    # Setup main Tkinter window
    root = tk.Tk()
    root.title("Secure Note-Taking App")
    root.geometry("600x400")

    # Display the login frame
    login_frame = LoginFrame(root, on_login, on_register)
    login_frame.pack(fill="both", expand=True)

    root.mainloop()
