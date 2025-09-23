import json
from note import Note
from config import EXPORT_PATH


def export_notes(notes, file_path=EXPORT_PATH):
    """
    Export a list of Note objects to a JSON file.
    """
    data = [note.to_dict() for note in notes]
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Exported {len(notes)} notes to {file_path}")


def import_notes(file_path=EXPORT_PATH):
    """
    Import notes from a JSON file and return a list of Note objects.
    """
    notes = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                notes.append(Note.from_dict(item))
        print(f"Imported {len(notes)} notes from {file_path}")
    except Exception as e:
        print(f"Error importing notes: {e}")
    return notes
