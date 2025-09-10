import json
import os
import tkinter as tk
from tkinter import messagebox
from news_api import NewsAPIClient
from ui import NewsApp


def load_config(config_path='config.json'):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


def main():
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return

    # Initialize the API client with configuration
    api_client = NewsAPIClient(
        endpoint=config.get('api_endpoint'),
        api_key=config.get('api_key'),
        country=config.get('country', 'us')
    )

    # Set up the Tkinter root window
    root = tk.Tk()
    root.title("Lightweight News Reader")
    root.geometry("800x600")

    # Create and start the UI
    app = NewsApp(root, api_client, refresh_interval=config.get('refresh_interval', 15))
    app.pack(fill='both', expand=True)

    # Start the Tkinter event loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application closed.")


if __name__ == '__main__':
    main()
