import tkinter as tk
import logger  # Initialize logging
from controller import ToDoController


def main():
    root = tk.Tk()
    app = ToDoController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
