import tkinter as tk
from view_main import MainView


def main():
    root = tk.Tk()
    root.title('Note Taking App')
    # Set a minimum size if needed
    root.geometry('800x600')
    app = MainView(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
