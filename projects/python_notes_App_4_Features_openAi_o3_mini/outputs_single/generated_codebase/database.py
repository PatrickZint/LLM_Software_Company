import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="notes.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            timestamp TEXT,
            categories TEXT,
            tags TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_note(self, title, content, categories="", tags=""):
        timestamp = datetime.now().isoformat()
        query = "INSERT INTO notes (title, content, timestamp, categories, tags) VALUES (?, ?, ?, ?, ?)"
        self.conn.execute(query, (title, content, timestamp, categories, tags))
        self.conn.commit()

    def update_note(self, note_id, title, content, categories="", tags=""):
        timestamp = datetime.now().isoformat()
        query = "UPDATE notes SET title=?, content=?, timestamp=?, categories=?, tags=? WHERE id=?"
        self.conn.execute(query, (title, content, timestamp, categories, tags, note_id))
        self.conn.commit()

    def delete_note(self, note_id):
        query = "DELETE FROM notes WHERE id=?"
        self.conn.execute(query, (note_id,))
        self.conn.commit()

    def get_all_notes(self):
        query = "SELECT * FROM notes ORDER BY timestamp DESC"
        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def search_notes(self, keyword):
        query = """
        SELECT * FROM notes 
        WHERE title LIKE ? OR content LIKE ? OR categories LIKE ? OR tags LIKE ?
        ORDER BY timestamp DESC
        """
        param = f"%{keyword}%"
        cursor = self.conn.execute(query, (param, param, param, param))
        return [dict(row) for row in cursor.fetchall()]

    def export_notes(self):
        notes = self.get_all_notes()
        return notes

    def import_notes(self, notes):
        for note in notes:
            # Expecting note to be a dict with keys: title, content, timestamp, categories, tags
            query = "INSERT INTO notes (title, content, timestamp, categories, tags) VALUES (?, ?, ?, ?, ?)"
            self.conn.execute(query, (
                note.get("title", ""),
                note.get("content", ""),
                note.get("timestamp", datetime.now().isoformat()),
                note.get("categories", ""),
                note.get("tags", "")
            ))
        self.conn.commit()
