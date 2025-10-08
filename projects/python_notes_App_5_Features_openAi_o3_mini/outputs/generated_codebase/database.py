'''Database module: Handles SQLite connection and schema initialization''' 

import sqlite3
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt BLOB NOT NULL
    );
    """)
    
    # Create notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content BLOB NOT NULL,
        timestamp TEXT NOT NULL,
        tags TEXT,
        categories TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)
    
    conn.commit()
    conn.close()


def add_user(username, password_hash, salt):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)", 
        (username, password_hash, salt)
    )
    conn.commit()
    conn.close()


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def add_note(user_id, title, content, timestamp, tags=None, categories=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notes (user_id, title, content, timestamp, tags, categories)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, title, content, timestamp, tags, categories))
    conn.commit()
    conn.close()


def get_notes(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes


def update_note(note_id, title, content, tags=None, categories=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE notes
        SET title = ?, content = ?, tags = ?, categories = ?
        WHERE id = ?
    """, (title, content, tags, categories, note_id))
    conn.commit()
    conn.close()


def delete_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
