import json
import os
from database import NoteDatabase
from gui import NotesApp


def load_config(config_file='config.json'):
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "DatabaseFilePath": "notes.db",
            "Theme": "light",
            "DefaultExportPath": "exports/",
            "SupportedFormats": {"RichText": True, "Markdown": True},
            "EditorSettings": {"FontSize": 14, "FontFamily": "Sans-Serif", "SyntaxHighlighting": True}
        }


def main():
    config = load_config()
    db_path = config.get("DatabaseFilePath", "notes.db")
    db = NoteDatabase(db_path)
    app = NotesApp(db, config)
    app.mainloop()


if __name__ == '__main__':
    main()
