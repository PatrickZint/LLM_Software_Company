import sqlite3
import datetime
from config import DB_PATH


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.initialize_database()
        
    def initialize_database(self):
        cursor = self.conn.cursor()
        # Create notes table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT
        );
        """)
        
        # Create categories table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        """)
        
        # Create tags table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        """)
        
        # Create note_categories table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS note_categories (
            note_id INTEGER,
            category_id INTEGER,
            FOREIGN KEY(note_id) REFERENCES notes(id),
            FOREIGN KEY(category_id) REFERENCES categories(id)
        );
        """)
        
        # Create note_tags table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS note_tags (
            note_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY(note_id) REFERENCES notes(id),
            FOREIGN KEY(tag_id) REFERENCES tags(id)
        );
        """)
        
        self.conn.commit()
        
    def create_note(self, title, content, categories=None, tags=None):
        if categories is None:
            categories = []
        if tags is None:
            tags = []
        now = datetime.datetime.now().isoformat()
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO notes (title, content, created_at)
        VALUES (?, ?, ?)
        """, (title, content, now))
        note_id = cursor.lastrowid
        
        self._update_note_metadata(note_id, categories, tags)
        self.conn.commit()
        return note_id
    
    def update_note(self, note_id, title, content, categories=None, tags=None):
        if categories is None:
            categories = []
        if tags is None:
            tags = []
        now = datetime.datetime.now().isoformat()
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE notes
        SET title = ?, content = ?, updated_at = ?
        WHERE id = ?
        """, (title, content, now, note_id))
        
        # Clear old metadata
        cursor.execute("DELETE FROM note_categories WHERE note_id = ?", (note_id,))
        cursor.execute("DELETE FROM note_tags WHERE note_id = ?", (note_id,))
        
        self._update_note_metadata(note_id, categories, tags)
        self.conn.commit()
        
    def delete_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM note_categories WHERE note_id = ?", (note_id,))
        cursor.execute("DELETE FROM note_tags WHERE note_id = ?", (note_id,))
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()
        
    def get_all_notes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        notes = []
        for row in cursor.fetchall():
            note = dict(row)
            note['categories'] = self.get_categories_for_note(row['id'])
            note['tags'] = self.get_tags_for_note(row['id'])
            notes.append(note)
        return notes
    
    def get_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        if row:
            note = dict(row)
            note['categories'] = self.get_categories_for_note(note_id)
            note['tags'] = self.get_tags_for_note(note_id)
            return note
        return None
    
    def search_notes(self, keyword):
        cursor = self.conn.cursor()
        like_keyword = f"%{keyword}%"
        cursor.execute("""
        SELECT * FROM notes 
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY created_at DESC
        """, (like_keyword, like_keyword))
        notes = []
        for row in cursor.fetchall():
            note = dict(row)
            note['categories'] = self.get_categories_for_note(row['id'])
            note['tags'] = self.get_tags_for_note(row['id'])
            notes.append(note)
        return notes
    
    def _update_note_metadata(self, note_id, categories, tags):
        cursor = self.conn.cursor()
        for cat in categories:
            cat = cat.strip()
            if cat:
                cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))
                cursor.execute("SELECT id FROM categories WHERE name = ?", (cat,))
                cat_row = cursor.fetchone()
                if cat_row:
                    cat_id = cat_row['id']
                    cursor.execute("INSERT INTO note_categories (note_id, category_id) VALUES (?, ?)", (note_id, cat_id))
        
        for tag in tags:
            tag = tag.strip()
            if tag:
                cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
                cursor.execute("SELECT id FROM tags WHERE name = ?", (tag,))
                tag_row = cursor.fetchone()
                if tag_row:
                    tag_id = tag_row['id']
                    cursor.execute("INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)", (note_id, tag_id))

    def get_categories_for_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT c.name FROM categories c
        INNER JOIN note_categories nc ON c.id = nc.category_id
        WHERE nc.note_id = ?
        """, (note_id,))
        return [row['name'] for row in cursor.fetchall()]
    
    def get_tags_for_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT t.name FROM tags t
        INNER JOIN note_tags nt ON t.id = nt.tag_id
        WHERE nt.note_id = ?
        """, (note_id,))
        return [row['name'] for row in cursor.fetchall()]
    
    def close(self):
        self.conn.close()
