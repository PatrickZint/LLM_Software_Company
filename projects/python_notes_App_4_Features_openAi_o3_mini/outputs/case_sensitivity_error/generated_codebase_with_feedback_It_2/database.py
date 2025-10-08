import sqlite3
import json
import os
from datetime import datetime
from models import Note


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
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            categories TEXT,
            tags TEXT
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_note(self, note: Note):
        now = datetime.now().isoformat()
        query = '''
        INSERT INTO notes (title, content, created_at, updated_at, categories, tags)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        cur = self.conn.execute(query, (note.title, note.content, now, now, note.categories, note.tags))
        self.conn.commit()
        return cur.lastrowid

    def get_all_notes(self):
        query = 'SELECT * FROM notes ORDER BY created_at DESC'
        cur = self.conn.execute(query)
        rows = cur.fetchall()
        notes = []
        for row in rows:
            note = Note(
                id=row['id'],
                title=row['title'],
                content=row['content'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                categories=row['categories'] if row['categories'] else '',
                tags=row['tags'] if row['tags'] else ''
            )
            notes.append(note)
        return notes

    def update_note(self, note: Note):
        now = datetime.now().isoformat()
        query = '''
        UPDATE notes
        SET title = ?, content = ?, updated_at = ?, categories = ?, tags = ?
        WHERE id = ?;
        '''
        self.conn.execute(query, (note.title, note.content, now, note.categories, note.tags, note.id))
        self.conn.commit()

    def delete_note(self, note_id: int):
        query = 'DELETE FROM notes WHERE id = ?'
        self.conn.execute(query, (note_id,))
        self.conn.commit()

    def export_notes(self, file_path: str):
        notes = self.get_all_notes()
        data = [note.to_dict() for note in notes]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def import_notes(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for note_data in data:
            note = Note.from_dict(note_data)
            # Check if note with same id exists; simple merge strategy
            if note.id is not None:
                self.conn.execute('''
                    INSERT OR REPLACE INTO notes (id, title, content, created_at, updated_at, categories, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                ''', (note.id, note.title, note.content, note.created_at, note.updated_at, note.categories, note.tags))
            else:
                self.add_note(note)
        self.conn.commit()

    def close(self):
        self.conn.close()
