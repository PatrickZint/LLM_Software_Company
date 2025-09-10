import unittest
from unittest.mock import patch
import requests
from news_api import NewsAPIClient


class TestNewsAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = NewsAPIClient(
            endpoint='https://newsapi.org/v2/top-headlines',
            api_key='dummy_key',
            country='us'
        )

    @patch('news_api.requests.get')
    def test_get_top_headlines_success(self, mock_get):
        # Setup a fake successful response
        fake_response = {
            'status': 'ok',
            'articles': [
                {
                    'title': 'Test Article',
                    'description': 'This is a test',
                    'publishedAt': '2023-10-10T12:34:56Z',
                    'url': 'http://example.com'
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = fake_response

        articles = self.client.get_top_headlines()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['title'], 'Test Article')
        self.assertIn('publishedAtReadable', articles[0])

    @patch('news_api.requests.get')
    def test_get_top_headlines_http_error(self, mock_get):
        # Setup a fake HTTP error
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError('Error')
        with self.assertRaises(Exception) as context:
            self.client.get_top_headlines()
        self.assertTrue('Network error occurred' in str(context.exception))

    @patch('news_api.requests.get')
    def test_get_top_headlines_api_failure(self, mock_get):
        # Setup a fake API response with error status
        fake_response = {
            'status': 'error',
            'message': 'Invalid API key'
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = fake_response

        with self.assertRaises(ValueError) as context:
            self.client.get_top_headlines()
        self.assertTrue('API returned error status' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
