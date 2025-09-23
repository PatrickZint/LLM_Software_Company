import os

# Base directory for the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the SQLite database file
DB_PATH = os.path.join(BASE_DIR, "notes.db")

# Default path for JSON export/import
EXPORT_PATH = os.path.join(BASE_DIR, "notes_export.json")
