import tkinter as tk
from ui import NoteApp


def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = NoteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
