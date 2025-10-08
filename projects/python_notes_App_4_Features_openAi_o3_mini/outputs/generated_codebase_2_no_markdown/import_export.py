import json
from config import EXPORT_PATH
from database import Database


def export_notes(db, file_path=EXPORT_PATH):
    """
    Export all notes (with metadata) to a JSON file.
    """
    notes = db.get_all_notes()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=4)
    return file_path


def import_notes(db, file_path):
    """
    Import notes from a JSON file and add them to the database.
    For simplicity, notes are always added new.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        notes = json.load(f)
    
    for note in notes:
        categories = note.get('categories', [])
        tags = note.get('tags', [])
        # Create note; duplicate handling can be improved if needed
        db.create_note(note['title'], note['content'], categories, tags)
