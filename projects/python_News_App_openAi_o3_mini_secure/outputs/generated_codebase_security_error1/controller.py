import tkinter as tk
import threading
import logging

from api_client import APIClient
from config_manager import ConfigManager
from ui_components import HeadlinesFrame, ArticleDetailFrame


class Controller:
    """Coordinates API calls, UI navigation, and user interactions."""
    def __init__(self, root):
        self.root = root
        self.root.title("News Reader")
        
        # Load configuration
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # Initialize the API client
        self.api_client = APIClient(self.config)
        
        # Store headlines data
        self.headlines = []

        # Create a container frame for swapping views
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        
        # Start with the headlines feed view
        self.current_frame = None
        self.show_headlines()

    def show_headlines(self):
        """Display the headlines feed screen."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = HeadlinesFrame(self.container, self)
        self.current_frame.pack(fill="both", expand=True)
        
        # Load headlines in a separate thread to avoid blocking the UI
        threading.Thread(target=self.load_headlines, daemon=True).start()

    def load_headlines(self):
        """Fetch headlines from the API and update the UI."""
        try:
            headlines = self.api_client.fetch_headlines()
            self.headlines = headlines
            # Schedule the UI update on the main thread
            self.current_frame.after(0, lambda: self.current_frame.update_headlines(headlines))
        except Exception as e:
            logging.error("Failed to load headlines: %s", e)
            self.current_frame.after(0, lambda: self.current_frame.show_error("Failed to load headlines. Please try again."))

    def show_article_detail(self, article):
        """Switch to the article detail view for a selected article."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ArticleDetailFrame(self.container, self, article)
        self.current_frame.pack(fill="both", expand=True)
