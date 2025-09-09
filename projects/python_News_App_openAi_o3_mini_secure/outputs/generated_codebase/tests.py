import unittest
from unittest.mock import patch

from news_api import NewsAPI


class TestNewsAPI(unittest.TestCase):
    @patch("news_api.requests.get")
    def test_get_top_headlines_success(self, mock_get):
        # Define a sample JSON response to simulate a successful API call
        mock_response = {
            "status": "ok",
            "totalResults": 1,
            "articles": [
                {
                    "title": "Test Article",
                    "description": "Test Description",
                    "publishedAt": "2023-10-01T12:00:00Z",
                    "source": {"name": "Test Source"},
                    "content": "Test full content"
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        news_api = NewsAPI()
        articles = news_api.get_top_headlines()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["title"], "Test Article")

    @patch("news_api.requests.get")
    def test_get_top_headlines_failure(self, mock_get):
        # Simulate a network error by raising an exception
        mock_get.side_effect = Exception("Network error")
        news_api = NewsAPI()
        with self.assertRaises(Exception):
            news_api.get_top_headlines()


if __name__ == "__main__":
    unittest.main()
