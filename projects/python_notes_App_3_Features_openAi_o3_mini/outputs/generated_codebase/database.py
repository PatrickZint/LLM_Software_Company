import sqlite3
from note import Note
from config import DB_PATH

class NoteDatabase:
    def __init__(self, db_path=DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        self.connection.commit()

    def add_note(self, note: Note):
        cursor = self.connection.cursor()
        note.created_at = Note.current_timestamp()
        note.updated_at = note.created_at
        cursor.execute('''
            INSERT INTO notes (title, content, category, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (note.title, note.content, note.category, note.tags, note.created_at, note.updated_at))
        self.connection.commit()
        note.id = cursor.lastrowid
        return note

    def get_all_notes(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM notes ORDER BY created_at DESC')
        rows = cursor.fetchall()
        notes = []
        for row in rows:
            note = Note(
                id=row['id'],
                title=row['title'],
                content=row['content'],
                category=row['category'],
                tags=row['tags'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            notes.append(note)
        return notes

    def get_note_by_id(self, note_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
        row = cursor.fetchone()
        if row:
            return Note(
                id=row['id'],
                title=row['title'],
                content=row['content'],
                category=row['category'],
                tags=row['tags'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        return None

    def update_note(self, note: Note):
        cursor = self.connection.cursor()
        note.updated_at = Note.current_timestamp()
        cursor.execute('''
            UPDATE notes
            SET title = ?, content = ?, category = ?, tags = ?, updated_at = ?
            WHERE id = ?
        ''', (note.title, note.content, note.category, note.tags, note.updated_at, note.id))
        self.connection.commit()
        return note

    def delete_note(self, note_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self.connection.commit()

    def search_notes(self, keyword):
        keyword = f"%{keyword}%"
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM notes
            WHERE title LIKE ? OR content LIKE ? OR category LIKE ? OR tags LIKE ?
            ORDER BY created_at DESC
        ''', (keyword, keyword, keyword, keyword))
        rows = cursor.fetchall()
        notes = []
        for row in rows:
            note = Note(
                id=row['id'],
                title=row['title'],
                content=row['content'],
                category=row['category'],
                tags=row['tags'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            notes.append(note)
        return notes

    def close(self):
        self.connection.close()
