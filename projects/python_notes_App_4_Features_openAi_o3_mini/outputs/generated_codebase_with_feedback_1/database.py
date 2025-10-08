import sqlite3
import datetime
import json

class NoteDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        query = '''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            categories TEXT,
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_note(self, title, content, categories="", tags=""):
        now = datetime.datetime.now().isoformat()
        query = '''
        INSERT INTO notes (title, content, categories, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        cur = self.conn.cursor()
        cur.execute(query, (title, content, categories, tags, now, now))
        self.conn.commit()
        return cur.lastrowid

    def get_all_notes(self):
        query = "SELECT * FROM notes ORDER BY created_at DESC;"
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def get_note_by_id(self, note_id):
        query = "SELECT * FROM notes WHERE id = ?;"
        cur = self.conn.cursor()
        cur.execute(query, (note_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def update_note(self, note_id, title, content, categories="", tags=""):
        now = datetime.datetime.now().isoformat()
        query = '''
        UPDATE notes
        SET title = ?, content = ?, categories = ?, tags = ?, updated_at = ?
        WHERE id = ?;
        '''
        self.conn.execute(query, (title, content, categories, tags, now, note_id))
        self.conn.commit()

    def delete_note(self, note_id):
        query = "DELETE FROM notes WHERE id = ?;"
        self.conn.execute(query, (note_id,))
        self.conn.commit()

    def search_notes(self, keyword):
        query = '''
        SELECT * FROM notes
        WHERE title LIKE ? OR content LIKE ? OR categories LIKE ? OR tags LIKE ?
        ORDER BY created_at DESC;
        '''
        pattern = f'%{keyword}%'
        cur = self.conn.cursor()
        cur.execute(query, (pattern, pattern, pattern, pattern))
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def export_notes(self, export_path):
        notes = self.get_all_notes()
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=4)

    def import_notes(self, import_path):
        with open(import_path, 'r', encoding='utf-8') as f:
            notes = json.load(f)
        for note in notes:
            # Simple merge strategy: if note with same title exists, update it
            existing = self.conn.execute("SELECT id FROM notes WHERE title = ?", (note['title'],)).fetchone()
            if existing:
                self.update_note(existing[0], note['title'], note['content'], note.get('categories', ''), note.get('tags', ''))
            else:
                self.add_note(note['title'], note['content'], note.get('categories', ''), note.get('tags', ''))
