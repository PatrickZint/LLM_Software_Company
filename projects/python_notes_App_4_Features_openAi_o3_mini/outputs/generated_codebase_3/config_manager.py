import json
import os

CONFIG_PATH = 'config.json'


class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        else:
            default_config = {
                'DatabaseFilePath': 'data/notes.db',
                'Theme': 'light',
                'DefaultExportPath': 'exports',
                'Editor': {
                    'font_size': 12,
                    'font_family': 'Arial',
                    'syntax_highlighting': True
                }
            }
            self.save_config(default_config)
            return default_config

    def save_config(self, config):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config(self.config)
