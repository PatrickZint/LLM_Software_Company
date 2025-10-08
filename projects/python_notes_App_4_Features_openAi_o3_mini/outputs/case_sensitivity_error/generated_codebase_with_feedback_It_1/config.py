import os

# Application configuration
# Adjust paths and settings as needed

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, 'data', 'notes.db')
DEFAULT_EXPORT_PATH = os.path.join(BASE_DIR, 'exports')
THEME = 'light'

# Editor Settings
EDITOR_SETTINGS = {
    'FontSize': 14,
    'FontFamily': 'Helvetica',
    'SyntaxHighlighting': True
}

# Supported Formats
SUPPORTED_FORMATS = {
    'RichText': True,
    'Markdown': True
}

# Ensure required directories exist
if not os.path.exists(os.path.join(BASE_DIR, 'data')):
    os.makedirs(os.path.join(BASE_DIR, 'data'))
if not os.path.exists(DEFAULT_EXPORT_PATH):
    os.makedirs(DEFAULT_EXPORT_PATH)
