import requests
import logging


class APIClient:
    """Handles API calls to the news service and parses responses."""
    def __init__(self, config):
        self.api_key = config.get("api_key")
        self.base_url = config.get("api_url")
        self.endpoint = config.get("endpoint", "/top-headlines")
        self.default_params = {}
        if "country" in config:
            self.default_params["country"] = config["country"]

    def fetch_headlines(self, params=None):
        url = self.base_url + self.endpoint
        headers = {"Authorization": self.api_key}
        # Merge default parameters with any provided parameters
        query_params = self.default_params.copy()
        if params:
            query_params.update(params)
        try:
            response = requests.get(url, headers=headers, params=query_params, timeout=5)
            response.raise_for_status()
            data = response.json()
            headlines = []
            for article in data.get("articles", []):
                headlines.append({
                    "headline": article.get("title"),
                    "summary": article.get("description"),
                    "publishedAt": article.get("publishedAt"),
                    "source": article.get("source", {}).get("name"),
                    "image_url": article.get("urlToImage")
                })
            return headlines
        except Exception as e:
            logging.error("Error fetching headlines: %s", e)
            raise
