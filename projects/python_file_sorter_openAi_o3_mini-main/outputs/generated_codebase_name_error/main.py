import threading
import time
import tkinter as tk
from tkinter import messagebox

import config
import gui
import file_monitor
import database


def start_file_monitor():
    # Start the file monitoring in a separate thread
    monitor = file_monitor.FileMonitor()
    monitor_thread = threading.Thread(target=monitor.start, daemon=True)
    monitor_thread.start()
    return monitor


def initialize_database():
    # Initialize the SQLite database for logging
    database.initialize_db()


if __name__ == '__main__':
    # Ensure configuration file exists/loaded
    config.load_config()
    
    # Initialize the logging database
    initialize_database()

    # Start file monitoring
    file_monitor_instance = start_file_monitor()
    
    # Launch the GUI
    root = tk.Tk()
    app = gui.FileOrganizerApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print('Application interrupted by user.')

    # Cleanup if necessary
    file_monitor_instance.stop()
    time.sleep(1)
    print('Application closed.')
