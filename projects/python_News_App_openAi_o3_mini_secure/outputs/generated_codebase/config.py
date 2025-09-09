import json
import os

CONFIG_FILE = "config.json"


def load_config():
    """
    Load configuration from an external JSON file.
    If the file does not exist, create one with default settings.
    Returns:
        dict: Configuration parameters.
    """
    if not os.path.exists(CONFIG_FILE):
        # Default configuration settings
        default_config = {
            "endpoint": "https://newsapi.org/v2/top-headlines?country=us",
            "api_key": "YOUR_API_KEY_HERE"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config
    else:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config
