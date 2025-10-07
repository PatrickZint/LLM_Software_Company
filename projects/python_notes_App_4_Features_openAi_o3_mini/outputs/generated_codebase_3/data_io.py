import json


def export_notes_json(notes, filepath):
    try:
        with open(filepath, 'w') as f:
            json.dump(notes, f, indent=4)
        return True
    except Exception as e:
        print(f'Export error: {e}')
        return False


def import_notes_json(filepath):
    try:
        with open(filepath, 'r') as f:
            notes = json.load(f)
        return notes
    except Exception as e:
        print(f'Import error: {e}')
        return None
