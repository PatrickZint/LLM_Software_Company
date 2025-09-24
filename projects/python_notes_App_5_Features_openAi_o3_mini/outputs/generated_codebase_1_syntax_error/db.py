import sqlite3
import os

class Database:
    def __init__(self, db_path='notes.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        // Future table definitions for categories and tags can be added here
        self.conn.commit()

    def add_note(self, title, content, created_at, updated_at):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO notes (title, content, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (title, content, created_at, updated_at))
        self.conn.commit()

    def get_all_notes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM notes ORDER BY created_at DESC')
        rows = cursor.fetchall()
        notes = [dict(row) for row in rows]
        return notes

    def get_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_note(self, note_id, title, content, updated_at):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?
        ''', (title, content, updated_at, note_id))
        self.conn.commit()

    def delete_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self.conn.commit()

    def search_notes(self, query):
        cursor = self.conn.cursor()
        like_query = f'%{query}%'
        cursor.execute('''
            SELECT * FROM notes
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY created_at DESC
        ''', (like_query, like_query))
        rows = cursor.fetchall()
        notes = [dict(row) for row in rows]
        return notes

    def close(self):
        if self.conn:
            self.conn.close()

if __name__ == '__main__':
    # For testing db functionality
    db = Database()
    db.add_note("Test Note", "This is a test.", "2023-10-01 12:00:00", "2023-10-01 12:00:00")
    notes = db.get_all_notes()
    print(notes)
    db.close()
