import requests

from config import load_config


class NewsAPI:
    def __init__(self):
        self.config = load_config()  # Load configuration from external file
        self.api_key = self.config.get("api_key")
        self.endpoint = self.config.get("endpoint")

        if not self.api_key or not self.endpoint:
            raise ValueError("API key or endpoint not configured properly in config.json.")

    def get_top_headlines(self):
        """Fetch top headlines using the configured public news API endpoint."""
        params = {
            "apiKey": self.api_key
        }
        try:
            response = requests.get(self.endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            return articles
        except requests.RequestException as e:
            raise Exception(f"Error fetching news: {str(e)}")
