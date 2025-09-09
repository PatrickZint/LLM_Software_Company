import tkinter as tk
import tkinter.messagebox as messagebox


class HomeScreen(tk.Frame):
    def __init__(self, master, controller, logger, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller
        self.logger = logger
        self.articles = []
        self.create_widgets()

    def create_widgets(self):
        # Refresh Button
        self.refresh_button = tk.Button(self, text='Refresh', command=self.controller.fetch_headlines)
        self.refresh_button.pack(pady=5)

        # Loading Label
        self.loading_label = tk.Label(self, text='', fg='blue')
        self.loading_label.pack()

        # Headlines Listbox with Scrollbar
        self.listbox_frame = tk.Frame(self)
        self.listbox_frame.pack(fill='both', expand=True)

        self.scrollbar = tk.Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side='right', fill='y')

        self.headlines_listbox = tk.Listbox(self.listbox_frame, yscrollcommand=self.scrollbar.set)
        self.headlines_listbox.pack(side='left', fill='both', expand=True)
        self.headlines_listbox.bind('<<ListboxSelect>>', self.on_article_select)
        self.scrollbar.config(command=self.headlines_listbox.yview)

    def show_loading(self):
        self.loading_label.config(text='Loading headlines...')

    def update_headlines(self, articles):
        self.loading_label.config(text='')
        self.headlines_listbox.delete(0, tk.END)
        self.articles = articles
        if not articles:
            self.show_error('No articles found.')
            return
        for idx, article in enumerate(articles):
            title = article.get('title', 'No Title')
            snippet = article.get('description', 'No Description')
            self.headlines_listbox.insert(tk.END, f'{title} - {snippet}')

    def show_error(self, message):
        self.loading_label.config(text='')
        self.logger.error(message)
        messagebox.showerror('Error', message)

    def on_article_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            article = self.articles[index]
            self.controller.show_article_detail(article)
