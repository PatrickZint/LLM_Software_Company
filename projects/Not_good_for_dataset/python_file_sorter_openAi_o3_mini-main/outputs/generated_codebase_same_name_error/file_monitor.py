import os
import time
from file_sorter import sort_file
from database import log_file_movement

class FileMonitor:
    def __init__(self, config):
        self.config = config
        self.directories = config.get('monitored_directories', [])
        self.interval = config.get('monitor_interval', 5)
        # To keep track of already seen files
        self.seen_files = {}
        for directory in self.directories:
            self.seen_files[directory] = set()

    def start_monitoring(self):
        print("Starting directory monitoring...")
        while True:
            for directory in self.directories:
                self.scan_directory(directory)
            time.sleep(self.interval)

    def scan_directory(self, directory):
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return
        try:
            current_files = set(os.listdir(directory))
            new_files = current_files - self.seen_files[directory]
            if new_files:
                for filename in new_files:
                    full_path = os.path.join(directory, filename)
                    if os.path.isfile(full_path):
                        # Process the new file
                        destination, rule_applied = sort_file(full_path, self.config)
                        if destination and rule_applied:
                            # Log the move
                            log_file_movement(full_path, destination, rule_applied)
            # Update seen files for the directory
            self.seen_files[directory] = current_files
        except Exception as e:
            print(f"Error scanning {directory}: {e}")

    def manual_trigger(self):
        # Allow manual scanning of directories
        for directory in self.directories:
            self.scan_directory(directory)
        print("Manual trigger complete.")
