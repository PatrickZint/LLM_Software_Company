import sqlite3
import datetime
import json
from config import DATABASE_FILE

class Database:
    def __init__(self, db_path=DATABASE_FILE):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created TIMESTAMP NOT NULL,
            updated TIMESTAMP NOT NULL,
            categories TEXT,
            tags TEXT
        );
        '''
        self.connection.execute(query)
        self.connection.commit()

    def add_note(self, title, content, categories='', tags=''):
        now = datetime.datetime.now()
        query = '''INSERT INTO notes (title, content, created, updated, categories, tags) 
                   VALUES (?, ?, ?, ?, ?, ?)'''
        cursor = self.connection.execute(query, (title, content, now, now, categories, tags))
        self.connection.commit()
        return cursor.lastrowid

    def update_note(self, note_id, title, content, categories='', tags=''):
        now = datetime.datetime.now()
        query = '''UPDATE notes SET title = ?, content = ?, updated = ?, categories = ?, tags = ? WHERE id = ?'''
        self.connection.execute(query, (title, content, now, categories, tags, note_id))
        self.connection.commit()

    def delete_note(self, note_id):
        query = 'DELETE FROM notes WHERE id = ?'
        self.connection.execute(query, (note_id,))
        self.connection.commit()

    def get_notes(self):
        query = 'SELECT * FROM notes ORDER BY updated DESC'
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def get_note_by_id(self, note_id):
        query = 'SELECT * FROM notes WHERE id = ?'
        cursor = self.connection.execute(query, (note_id,))
        return cursor.fetchone()

    def search_notes(self, keyword):
        like_keyword = f'%{keyword}%'
        query = '''
        SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? OR categories LIKE ? OR tags LIKE ?
        ORDER BY updated DESC
        '''
        cursor = self.connection.execute(query, (like_keyword, like_keyword, like_keyword, like_keyword))
        return cursor.fetchall()

    def export_notes(self, note_ids=None):
        # If note_ids is provided, export only these; else export all notes
        if note_ids:
            placeholder = ','.join('?' for _ in note_ids)
            query = f'SELECT * FROM notes WHERE id IN ({placeholder})'
            cursor = self.connection.execute(query, note_ids)
        else:
            query = 'SELECT * FROM notes'
            cursor = self.connection.execute(query)
        notes = [dict(row) for row in cursor.fetchall()]
        return json.dumps(notes, default=str, indent=2)

    def import_notes(self, json_data):
        try:
            notes = json.loads(json_data)
            for note in notes:
                # Check if note exists based on title and created timestamp 
                # For simplicity, we insert all imported notes
                self.add_note(
                    title=note.get('title', 'Untitled'),
                    content=note.get('content', ''),
                    categories=note.get('categories', ''),
                    tags=note.get('tags', '')
                )
            return True
        except Exception as e:
            print('Error importing notes:', e)
            return False
