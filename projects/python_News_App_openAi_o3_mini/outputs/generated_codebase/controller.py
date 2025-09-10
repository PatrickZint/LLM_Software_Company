import threading
from api_service import APIService


class Controller:
    def __init__(self, config, logger):
        self.logger = logger
        self.config = config
        self.api_service = APIService(config, logger)
        self.home_screen = None
        # Auto-refresh interval in seconds
        self.refresh_interval = int(config.get('refresh_interval', 300))
        self.auto_refresh_timer = None

    def set_home_screen(self, home_screen):
        self.home_screen = home_screen

    def fetch_headlines(self):
        if self.home_screen:
            self.home_screen.show_loading()

        def task():
            try:
                articles = self.api_service.fetch_headlines()
                # Update UI on the main thread
                self.home_screen.after(0, lambda: self.home_screen.update_headlines(articles))
                self.logger.info('Fetched headlines successfully.')
            except Exception as e:
                self.home_screen.after(0, lambda: self.home_screen.show_error(f'Error fetching headlines: {e}'))
            finally:
                # Schedule auto-refresh if enabled
                self.schedule_auto_refresh()

        # Run the API call in a separate thread to avoid UI freeze
        threading.Thread(target=task, daemon=True).start()

    def schedule_auto_refresh(self):
        if self.refresh_interval > 0:
            if self.auto_refresh_timer:
                self.auto_refresh_timer.cancel()
            self.logger.info(f'Scheduling auto refresh in {self.refresh_interval} seconds.')
            self.auto_refresh_timer = threading.Timer(self.refresh_interval, self.fetch_headlines)
            self.auto_refresh_timer.start()

    def cancel_auto_refresh(self):
        if self.auto_refresh_timer:
            self.auto_refresh_timer.cancel()
            self.auto_refresh_timer = None

    def show_article_detail(self, article):
        # Open a new window for article detail
        import ui_detail
        detail_view = ui_detail.DetailView(article, self.logger, self.home_screen.master)
        detail_view.grab_set()
