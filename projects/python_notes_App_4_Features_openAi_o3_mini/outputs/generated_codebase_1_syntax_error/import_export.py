import json
from datetime import datetime

def export_notes(db, export_path):
    # Retrieve all notes from the database
    notes = db.get_all_notes()
    # Write notes to the specified JSON file
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=4)


def import_notes(db, import_path, merge=True):
    # Load notes from the JSON file
    with open(import_path, 'r', encoding='utf-8') as f:
        notes = json.load(f)

    # If not merging, clear existing notes
    if not merge:
        cursor = db.conn.cursor()
        cursor.execute('DELETE FROM notes')
        db.conn.commit()

    # Insert or update notes
    for note in notes:
        # Try to find an existing note with the same title and created_at
        query = "SELECT id FROM notes WHERE title = ? AND created_at = ?"
        cursor = db.conn.cursor()
        cursor.execute(query, (note['title'], note.get('created_at', '')))
        row = cursor.fetchone()
        if row:
            # Update the note
            note_id = row[0]
            update_query = "UPDATE notes SET content = ?, updated_at = ? WHERE id = ?"
            cursor.execute(update_query, (note['content'], note.get('updated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')), note_id))
        else:
            # Insert new note
            insert_query = "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)"
            cursor.execute(insert_query, (
                note['title'],
                note['content'],
                note.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                note.get('updated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ))
    db.conn.commit()
