import json
import os

CONFIG_FILE = 'config.json'


def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file '{CONFIG_FILE}' not found.")
    with open(CONFIG_FILE, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Configuration file '{CONFIG_FILE}' is not valid JSON: {e}")
    return config


if __name__ == '__main__':
    config = load_config()
    print(json.dumps(config, indent=2))
