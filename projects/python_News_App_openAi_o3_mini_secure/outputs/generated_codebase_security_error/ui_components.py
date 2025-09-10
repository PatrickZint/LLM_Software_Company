import tkinter as tk
from tkinter import messagebox, ttk


class HeadlinesFrame(tk.Frame):
    """The main screen displaying a scrollable list of news headlines."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        title = tk.Label(self, text="Top Headlines", font=("Arial", 16))
        title.pack(pady=10)
        
        # Loading indicator
        self.loading_label = tk.Label(self, text="Loading...", font=("Arial", 12))
        self.loading_label.pack(pady=5)
        
        # Create a scrollable frame for the list of headlines
        self.list_container = tk.Frame(self)
        self.list_container.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.list_container)
        self.scrollbar = ttk.Scrollbar(self.list_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Ensure the canvas scrolls with the content
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.headline_buttons = []

    def update_headlines(self, headlines):
        """Populate the UI with the list of headlines."""
        # Remove loading indicator
        if self.loading_label:
            self.loading_label.destroy()
        
        # Create a button for each headline
        for article in headlines:
            btn_text = f"{article.get('headline')} ({article.get('source')})"
            btn = tk.Button(
                self.scrollable_frame,
                text=btn_text,
                wraplength=750,
                anchor="w",
                justify="left",
                command=lambda a=article: self.controller.show_article_detail(a)
            )
            btn.pack(fill="x", padx=5, pady=2)
            
            # Add a simple hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="lightgray"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="SystemButtonFace"))
            
            self.headline_buttons.append(btn)

    def show_error(self, message):
        """Display an error message to the user."""
        messagebox.showerror("Error", message)


class ArticleDetailFrame(tk.Frame):
    """The detailed view for a selected article."""
    def __init__(self, parent, controller, article):
        super().__init__(parent)
        self.controller = controller
        
        # Extract article details
        headline = article.get("headline", "No Title")
        summary = article.get("summary", "No Content")
        publishedAt = article.get("publishedAt", "Unknown Date")
        source = article.get("source", "Unknown Source")
        image_url = article.get("image_url", "")
        
        # Headline
        tk.Label(self, text=headline, font=("Arial", 16, "bold"), wraplength=750).pack(pady=10)
        
        # Source and publication date
        tk.Label(self, text=f"Source: {source} | {publishedAt}", font=("Arial", 10)).pack(pady=5)
        
        # Article summary/content
        summary_text = tk.Text(self, wrap="word", height=10)
        summary_text.insert("1.0", summary)
        summary_text.config(state="disabled")
        summary_text.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Back button
        tk.Button(self, text="Back", command=self.controller.show_headlines).pack(pady=10)
