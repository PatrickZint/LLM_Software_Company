import sqlite3
import os

DB_NAME = 'notes_app.db'


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Create notes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content BLOB NOT NULL,
            timestamp TEXT NOT NULL,
            tags TEXT,
            categories TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()


def add_user(username, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def add_note(user_id, title, content, timestamp, tags, categories):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO notes (user_id, title, content, timestamp, tags, categories)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, title, content, timestamp, tags, categories))
    conn.commit()
    conn.close()


def update_note(note_id, title, content, timestamp, tags, categories):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE notes
        SET title=?, content=?, timestamp=?, tags=?, categories=?
        WHERE id=?
    ''', (title, content, timestamp, tags, categories, note_id))
    conn.commit()
    conn.close()


def delete_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id=?', (note_id,))
    conn.commit()
    conn.close()


def get_notes(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE user_id=? ORDER BY timestamp DESC', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_note_by_id(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE id=?', (note_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def search_notes(user_id, query):
    conn = get_connection()
    cursor = conn.cursor()
    if query.strip() == "":
        cursor.execute('SELECT * FROM notes WHERE user_id=? ORDER BY timestamp DESC', (user_id,))
    else:
        like_query = f'%{query}%' 
        cursor.execute('''
            SELECT * FROM notes 
            WHERE user_id=? AND (title LIKE ? OR tags LIKE ? OR categories LIKE ? OR timestamp LIKE ?)
            ORDER BY timestamp DESC
        ''', (user_id, like_query, like_query, like_query, like_query))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
