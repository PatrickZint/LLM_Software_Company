import tkinter as tk
from auth import LoginWindow
from note_app import NoteApp


def main():
    root = tk.Tk()
    root.title("Note App - Login")
    root.geometry("300x200")

    # Start with login window
    login_window = LoginWindow(root, on_success=launch_app)

    root.mainloop()


def launch_app(user, encryption_key):
    # Destroys the current window widgets and launches the note app UI
    root = tk._default_root
    for widget in root.winfo_children():
        widget.destroy()
    app = NoteApp(user, encryption_key)
    app.mainloop()


if __name__ == '__main__':
    main()
