import os

# Base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the SQLite database file
DB_PATH = os.path.join(BASE_DIR, "notes.db")

# Default export path for JSON backup files
EXPORT_PATH = os.path.join(BASE_DIR, "notes_export.json")
