import json
import os
from security import decrypt


class ConfigManager:
    """Handles loading and decrypting the configuration settings."""
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = None

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file {self.config_path} not found.")
        with open(self.config_path, "r") as f:
            self.config = json.load(f)
            
        # If the config indicates that sensitive data is encrypted, decrypt it
        if self.config.get("encrypted", False) and "api_key" in self.config:
            self.config["api_key"] = decrypt(self.config["api_key"])

        return self.config
