import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import webbrowser


class NewsApp(tk.Frame):
    def __init__(self, master, api_client, refresh_interval=15):
        super().__init__(master)
        self.master = master
        self.api_client = api_client
        self.refresh_interval_ms = refresh_interval * 60 * 1000  # Convert minutes to milliseconds
        self.articles = []

        self.create_widgets()
        self.fetch_articles_async()

    def create_widgets(self):
        # Create a top frame for Refresh button
        top_frame = tk.Frame(self)
        top_frame.pack(side='top', fill='x', padx=10, pady=5)

        refresh_btn = tk.Button(top_frame, text='Refresh', command=self.fetch_articles_async)
        refresh_btn.pack(side='right')

        # Create a canvas with a scrollbar for the list of headlines
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # Label for status / error messages
        self.status_label = tk.Label(self, text='', fg='red')
        self.status_label.pack(side='bottom', fill='x', padx=10, pady=5)

    def fetch_articles_async(self):
        self.status_label.config(text='Loading...')
        thread = threading.Thread(target=self.fetch_articles)
        thread.start()

    def fetch_articles(self):
        try:
            articles = self.api_client.get_top_headlines()
            # Update articles on the UI thread
            self.master.after(0, self.update_articles, articles)
        except Exception as e:
            self.master.after(0, self.show_error, str(e))

    def update_articles(self, articles):
        # Clear current items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.articles = articles

        if not articles:
            self.status_label.config(text='No articles found.')
            return
        else:
            self.status_label.config(text='')

        # Create a frame for each article
        for idx, article in enumerate(articles):
            frame = ttk.Frame(self.scrollable_frame, relief='ridge', borderwidth=1, padding=5)
            frame.pack(fill='x', padx=5, pady=5)
            frame.bind("<Button-1>", lambda e, idx=idx: self.open_detail(idx))

            # Article title
            title = article.get('title', 'No Title')
            title_label = ttk.Label(frame, text=title, font=('Helvetica', 12, 'bold'))
            title_label.pack(anchor='w')
            title_label.bind("<Button-1>", lambda e, idx=idx: self.open_detail(idx))

            # Publication Date
            pub_date = article.get('publishedAtReadable', '')
            date_label = ttk.Label(frame, text=pub_date, font=('Helvetica', 10, 'italic'))
            date_label.pack(anchor='w')

            # Snippet (using description as snippet if available)
            snippet = article.get('description', 'No description available.')
            snippet_label = ttk.Label(frame, text=snippet, wraplength=750, justify='left')
            snippet_label.pack(anchor='w')

    def show_error(self, error_message):
        self.status_label.config(text=f"Error: {error_message}")
        retry = messagebox.askretrycancel("Error", f"Failed to fetch news:\n{error_message}\nDo you want to retry?")
        if retry:
            self.fetch_articles_async()

    def open_detail(self, idx):
        article = self.articles[idx]
        detail_window = tk.Toplevel(self.master)
        detail_window.title(article.get('title', 'Article Detail'))
        detail_window.geometry('600x400')

        # Title
        title_label = ttk.Label(detail_window, text=article.get('title', 'No Title'), font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=10, anchor='center')

        # Publication Date
        pub_date = article.get('publishedAtReadable', '')
        date_label = ttk.Label(detail_window, text=pub_date, font=('Helvetica', 10, 'italic'))
        date_label.pack(pady=5)

        # Content / Description
        content = article.get('content') or article.get('description', 'No content available.')
        content_text = tk.Text(detail_window, wrap='word')
        content_text.insert('1.0', content)
        content_text.config(state='disabled')
        content_text.pack(expand=True, fill='both', padx=10, pady=10)

        # Read more link if URL is available
        url = article.get('url')
        if url:
            def open_url(event=None, url=url):
                webbrowser.open(url)
            link = ttk.Label(detail_window, text='Read more...', foreground='blue', cursor='hand2')
            link.pack(pady=5)
            link.bind("<Button-1>", open_url)

        # A close button
        close_btn = ttk.Button(detail_window, text='Close', command=detail_window.destroy)
        close_btn.pack(pady=5)

        # Center the detail window on screen
        detail_window.transient(self.master)
        detail_window.grab_set()
        self.master.wait_window(detail_window)

    def schedule_refresh(self):
        # Schedule next refresh
        self.master.after(self.refresh_interval_ms, self.fetch_articles_async)

    # Override pack so that we can schedule periodic refreshes after packing
    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.schedule_refresh()
