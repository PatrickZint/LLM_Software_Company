import tkinter as tk
from controller import Controller
from logger import setup_logging


def main():
    # Initialize logging
    setup_logging()
    
    # Create the main Tkinter window
    root = tk.Tk()
    root.geometry('800x600')
    
    # Instantiate the Controller, which sets up the UI and API client
    app = Controller(root)
    
    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
