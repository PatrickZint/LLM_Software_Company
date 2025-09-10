import time
import threading
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config
import rule_engine

class FileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def process(self, file_path):
        # Apply rules to the detected file.
        cfg = config.get_config()
        rule_engine.apply_rules(file_path, cfg)

class FileMonitor:
    def __init__(self):
        self.observer = Observer()
        self.running = False

    def start(self):
        self.running = True
        cfg = config.get_config()
        directories = cfg.get('monitored_directories', [])
        event_handler = FileEventHandler()

        for directory in directories:
            if os.path.isdir(directory):
                self.observer.schedule(event_handler, directory, recursive=False)
            else:
                print(f"Directory does not exist: {directory}")

        self.observer.start()
        try:
            while self.running:
                time.sleep(cfg.get('monitoring', {}).get('polling_interval', 1))
        except Exception as e:
            print(f"Monitor error: {e}")
        finally:
            self.observer.stop()
            self.observer.join()

    def stop(self):
        self.running = False
