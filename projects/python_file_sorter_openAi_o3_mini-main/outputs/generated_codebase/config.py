import json
import os

# Configuration file path
CONFIG_FILE = 'config.json'

# Default configuration
DEFAULT_CONFIG = {
    "monitored_directories": [ ],
    "rules": {
        "file_type": {
            ".txt": "organized/text_files",
            ".jpg": "organized/images",
            ".png": "organized/images"
        },
        "creation_date": {
            "enabled": true,
            "path_template": "organized/{year}/{month}"
        }
    },
    "database": {
        "name": "file_organizer.db"
    },
    "report": {
        "export_path": "reports/"
    },
    "monitoring": {
        "polling_interval": 1
    }
}

_config = None


def load_config():
    global _config
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        _config = DEFAULT_CONFIG
    else:
        try:
            with open(CONFIG_FILE, 'r') as f:
                _config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            _config = DEFAULT_CONFIG
    return _config


def get_config():
    global _config
    if _config is None:
        return load_config()
    return _config


def save_config(cfg):
    global _config
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(cfg, f, indent=4)
        _config = cfg
    except Exception as e:
        print(f"Error saving config: {e}")


if __name__ == '__main__':
    # For testing purposes, print the current configuration
    cfg = load_config()
    print(json.dumps(cfg, indent=4))
