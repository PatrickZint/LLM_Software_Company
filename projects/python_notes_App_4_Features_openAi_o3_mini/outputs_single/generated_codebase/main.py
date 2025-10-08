import tkinter as tk
from ui import NoteApp


def main():
    root = tk.Tk()
    root.title("Simple Note Taking App")
    app = NoteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
