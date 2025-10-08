import json
import db


def export_notes_to_json(filename):
    notes = db.get_all_notes()
    notes_list = []
    for note in notes:
        notes_list.append({
            "id": note["id"],
            "title": note["title"],
            "content": note["content"],
            "category": note["category"],
            "tags": note["tags"],
            "timestamp": note["timestamp"]
        })
    with open(filename, 'w') as f:
        json.dump(notes_list, f, indent=4)


def import_notes_from_json(filename):
    with open(filename, 'r') as f:
        notes_list = json.load(f)
    for note in notes_list:
        title = note.get("title", "")
        content = note.get("content", "")
        category = note.get("category", "")
        tags = note.get("tags", "")
        db.add_note(title, content, category, tags)
