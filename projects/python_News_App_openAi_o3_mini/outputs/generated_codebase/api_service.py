import requests


class APIService:
    def __init__(self, config, logger):
        self.endpoint = config.get('api_endpoint')
        self.api_key = config.get('api_key')
        self.logger = logger

        if not self.endpoint or not self.api_key:
            raise ValueError('API endpoint or API key is missing in the configuration.')

    def fetch_headlines(self):
        params = {
            'apiKey': self.api_key,
            'country': 'us'
        }
        try:
            response = requests.get(self.endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            # Validate response structure
            if 'articles' not in data:
                raise ValueError('Invalid data structure: "articles" key not found.')
            return data['articles']
        except requests.RequestException as e:
            self.logger.error(f'API request failed: {e}')
            raise
        except ValueError as ve:
            self.logger.error(f'Error processing data: {ve}')
            raise
