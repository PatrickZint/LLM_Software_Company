import requests
import datetime


class NewsAPIClient:
    def __init__(self, endpoint, api_key, country='us'):
        self.endpoint = endpoint
        self.api_key = api_key
        self.country = country

    def get_top_headlines(self):
        params = {
            'apiKey': self.api_key,
            'country': self.country
        }
        try:
            response = requests.get(self.endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('status') != 'ok':
                raise ValueError('API returned error status')
            # Optional: Convert publication date into human readable format
            for article in data.get('articles', []):
                if article.get('publishedAt'):
                    article['publishedAtReadable'] = self._format_date(article.get('publishedAt'))
            return data.get('articles', [])
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Network error occurred: {e}")
        except ValueError as ve:
            raise ValueError(f"Failed to retrieve articles: {ve}")

    def _format_date(self, date_str):
        try:
            # Example: '2023-10-10T12:34:56Z'
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime("%b %d, %Y %I:%M %p")
        except Exception:
            return date_str
