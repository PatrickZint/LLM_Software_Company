import sqlite3

DB_PATH = "notes_app.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash BLOB,
            encryption_salt BLOB
        )
    ''')
    
    # Create notes table
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content BLOB,
            timestamp TEXT,
            tags TEXT,
            category TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None


def create_user(username, password_hash, encryption_salt):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash, encryption_salt) VALUES (?, ?, ?)", (username, password_hash, encryption_salt))
    conn.commit()
    conn.close()


def create_note(user_id, title, content, timestamp, tags, category):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO notes (user_id, title, content, timestamp, tags, category) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, title, content, timestamp, tags, category))
    conn.commit()
    conn.close()


def update_note(note_id, title, content, timestamp, tags, category):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE notes SET title = ?, content = ?, timestamp = ?, tags = ?, category = ? WHERE id = ?",
              (title, content, timestamp, tags, category, note_id))
    conn.commit()
    conn.close()


def delete_note(note_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()


def get_notes_by_user(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,))
    notes = c.fetchall()
    conn.close()
    return [dict(note) for note in notes]


def search_notes(user_id, query):
    conn = get_connection()
    c = conn.cursor()
    q = f"%{query}%"
    c.execute("SELECT * FROM notes WHERE user_id = ? AND (title LIKE ? OR content LIKE ? OR tags LIKE ? OR category LIKE ?)",
              (user_id, q, q, q, q))
    notes = c.fetchall()
    conn.close()
    return [dict(note) for note in notes]


# Initialize database when module is loaded
init_db()
