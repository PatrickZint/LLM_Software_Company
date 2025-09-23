import tkinter as tk
from ui import NoteAppUI


def main():
    root = tk.Tk()
    app = NoteAppUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
