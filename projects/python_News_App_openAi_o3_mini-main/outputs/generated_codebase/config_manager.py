import json
import os


class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = {}
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f'Configuration file {self.config_file} not found.')
        with open(self.config_file, 'r') as f:
            try:
                self.config = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f'Error parsing the configuration file: {e}')

    def get(self, key, default=None):
        return self.config.get(key, default)
