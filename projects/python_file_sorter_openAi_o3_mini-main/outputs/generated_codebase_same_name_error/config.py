import json
import os

CONFIG_FILE = 'config.json'

DEFAULT_CONFIG = {
    "monitored_directories": ["/path/to/monitor"],
    "sorting_rules": {
        "by_file_type": true,
        "by_creation_date": true
    },
    "database": {
        "path": "file_logs.db"
    },
    "csv_export": {
        "export_path": "logs_export.csv"
    },
    "monitor_interval": 5
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None


def create_default_config():
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print(f"Default configuration created at {CONFIG_FILE}")
    except Exception as e:
        print(f"Failed to create default config: {e}")
