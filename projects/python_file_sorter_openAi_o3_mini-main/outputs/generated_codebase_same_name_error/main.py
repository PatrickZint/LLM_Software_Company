import threading
import time
from config import load_config, create_default_config
from file_monitor import FileMonitor
from ui import start_ui
import database


def main():
    # Load or create default configuration
    config = load_config()
    if config is None:
        create_default_config()
        config = load_config()
    
    # Initialize the database (default filename from config or fallback)
    db_path = config.get('database', {}).get('path', 'file_logs.db')
    database.initialize_db(db_path)

    # Start the file monitor in a background thread
    monitor = FileMonitor(config)
    monitor_thread = threading.Thread(target=monitor.start_monitoring, daemon=True)
    monitor_thread.start()

    # Start the UI (blocking call)
    start_ui(config, monitor, db_path)


if __name__ == "__main__":
    main()
