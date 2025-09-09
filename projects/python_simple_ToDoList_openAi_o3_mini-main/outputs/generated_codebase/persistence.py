import json
import os
import logging


class FileManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def load_data(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return data
        except Exception as e:
            logging.error("Error loading data: %s", e)
            return []

    def save_data(self, data):
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            logging.error("Error saving data: %s", e)
