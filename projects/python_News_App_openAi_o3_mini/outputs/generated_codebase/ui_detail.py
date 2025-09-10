import tkinter as tk
import tkinter.messagebox as messagebox
import webbrowser


class DetailView(tk.Toplevel):
    def __init__(self, article, logger, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.article = article
        self.logger = logger
        self.title(article.get('title', 'Article Detail'))
        self.geometry('600x400')
        self.create_widgets()

    def create_widgets(self):
        # Article Title
        title = self.article.get('title', 'No Title')
        self.title_label = tk.Label(self, text=title, font=('Arial', 16, 'bold'))
        self.title_label.pack(pady=10)

        # Article Metadata
        metadata = ''
        author = self.article.get('author')
        published_at = self.article.get('publishedAt')
        if author:
            metadata += f'Author: {author}  '
        if published_at:
            metadata += f'Published: {published_at}'
        self.metadata_label = tk.Label(self, text=metadata, font=('Arial', 10))
        self.metadata_label.pack(pady=5)

        # Article Content
        content = self.article.get('content', 'Full content not available.')
        self.content_text = tk.Text(self, wrap='word', height=10)
        self.content_text.insert(tk.END, content)
        self.content_text.config(state='disabled')
        self.content_text.pack(padx=10, pady=10, fill='both', expand=True)

        # Link to original article
        url = self.article.get('url')
        if url:
            self.link_button = tk.Button(self, text='Read Full Article', command=lambda: self.open_link(url))
            self.link_button.pack(pady=5)

        # Back Button
        self.back_button = tk.Button(self, text='Back', command=self.destroy)
        self.back_button.pack(pady=5)

    def open_link(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            self.logger.error(f'Failed to open URL: {e}')
            messagebox.showerror('Error', 'Failed to open the link.')
