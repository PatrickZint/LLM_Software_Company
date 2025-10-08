import sqlite3
import os
import json
from datetime import datetime

# Define the database path
DB_PATH = 'data/notes.db'


class NoteDAO:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Create Notes table with additional columns for categories and tags
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TEXT,
                updated_at TEXT,
                categories TEXT,
                tags TEXT
            )
        ''')
        self.conn.commit()

    def get_all_notes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM Notes ORDER BY created_at DESC')
        rows = cursor.fetchall()
        notes = []
        for row in rows:
            notes.append({
                'id': row['id'],
                'title': row['title'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'categories': json.loads(row['categories']) if row['categories'] else [],
                'tags': json.loads(row['tags']) if row['tags'] else []
            })
        return notes

    def get_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM Notes WHERE id=?', (note_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row['id'],
                'title': row['title'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'categories': json.loads(row['categories']) if row['categories'] else [],
                'tags': json.loads(row['tags']) if row['tags'] else []
            }
        return None

    def create_note(self, note):
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        categories_json = json.dumps(note.get('categories', []))
        tags_json = json.dumps(note.get('tags', []))
        cursor.execute('''
            INSERT INTO Notes (title, content, created_at, updated_at, categories, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (note['title'], note['content'], now, now, categories_json, tags_json))
        self.conn.commit()
        return cursor.lastrowid

    def update_note(self, note_id, note):
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        categories_json = json.dumps(note.get('categories', []))
        tags_json = json.dumps(note.get('tags', []))
        cursor.execute('''
            UPDATE Notes
            SET title=?, content=?, updated_at=?, categories=?, tags=?
            WHERE id=?
        ''', (note['title'], note['content'], now, categories_json, tags_json, note_id))
        self.conn.commit()

    def delete_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM Notes WHERE id=?', (note_id,))
        self.conn.commit()

    def search_notes(self, keyword):
        cursor = self.conn.cursor()
        # Using wildcards for LIKE search on title, content, categories, tags
        pattern = f'%{keyword}%'
        cursor.execute('''
            SELECT * FROM Notes
            WHERE title LIKE ? OR content LIKE ? OR categories LIKE ? OR tags LIKE ?
            ORDER BY created_at DESC
        ''', (pattern, pattern, pattern, pattern))
        rows = cursor.fetchall()
        notes = []
        for row in rows:
            notes.append({
                'id': row['id'],
                'title': row['title'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'categories': json.loads(row['categories']) if row['categories'] else [],
                'tags': json.loads(row['tags']) if row['tags'] else []
            })
        return notes
