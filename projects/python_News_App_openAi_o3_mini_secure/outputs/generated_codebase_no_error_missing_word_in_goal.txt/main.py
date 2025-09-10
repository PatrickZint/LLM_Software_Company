import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

from news_api import NewsAPI
from config import load_config


class NewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lightweight News Reader")
        self.news_api = NewsAPI()

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Loading label
        self.loading_label = ttk.Label(self.main_frame, text="Loading headlines...")
        self.loading_label.pack()

        # Listbox for headlines
        self.headlines_list = tk.Listbox(self.main_frame, height=15)
        self.headlines_list.pack(expand=True, fill=tk.BOTH, pady=5)
        self.headlines_list.bind("<<ListboxSelect>>", self.on_headline_select)

        # Refresh button
        self.refresh_button = ttk.Button(self.main_frame, text="Refresh", command=self.load_headlines)
        self.refresh_button.pack(pady=5)

        self.headlines_data = []  # Will store list of articles

        # Initially load headlines
        self.load_headlines()

    def load_headlines(self):
        self.loading_label.config(text="Loading headlines...")
        self.root.update_idletasks()
        try:
            articles = self.news_api.get_top_headlines()
            self.headlines_list.delete(0, tk.END)
            self.headlines_data = articles
            if not articles:
                self.loading_label.config(text="No headlines available.")
            else:
                self.loading_label.config(text="Select an article to view details.")
                for idx, article in enumerate(articles):
                    title = article.get("title", "No Title")
                    timestamp = article.get("publishedAt", "")
                    display_text = f"{title} ({timestamp})" if timestamp else title
                    self.headlines_list.insert(tk.END, display_text)
        except Exception as e:
            self.loading_label.config(text="Error fetching news")
            messagebox.showerror("Error", f"Failed to load headlines: {str(e)}")

    def on_headline_select(self, event):
        if not self.headlines_list.curselection():
            return  
        index = self.headlines_list.curselection()[0]
        article = self.headlines_data[index]
        self.open_article_detail(article)

    def open_article_detail(self, article):
        detail_window = tk.Toplevel(self.root)
        detail_window.title(article.get("title", "Article Detail"))
        frame = ttk.Frame(detail_window, padding="10")
        frame.pack(expand=True, fill=tk.BOTH)

        # Title
        title_label = ttk.Label(frame, text=article.get("title", "No Title"), font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 10))

        # Description
        description = article.get("description", "No Description Available")
        desc_label = ttk.Label(frame, text=description, wraplength=600, justify="left")
        desc_label.pack(pady=(0, 10))

        # Content
        content = article.get("content")
        if content:
            content_label = ttk.Label(frame, text=content, wraplength=600, justify="left")
            content_label.pack(pady=(0, 10))

        # Publication info
        pub_date = article.get("publishedAt", "")
        source = article.get("source", {}).get("name", "Unknown Source")
        info_label = ttk.Label(frame, text=f"Published at: {pub_date} | Source: {source}")
        info_label.pack(pady=(0, 10))

        # Back/Close button
        close_button = ttk.Button(frame, text="Close", command=detail_window.destroy)
        close_button.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = NewsApp(root)
    root.mainloop()
