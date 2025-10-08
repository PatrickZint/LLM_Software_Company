import sqlite3


def connect_db(db_name='notes.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            tags TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def add_note(title, content, category, tags):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (title, content, category, tags) VALUES (?,?,?,?)",
        (title, content, category, tags)
    )
    conn.commit()
    conn.close()


def update_note(note_id, title, content, category, tags):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notes SET title=?, content=?, category=?, tags=?, timestamp=CURRENT_TIMESTAMP WHERE id=?",
        (title, content, category, tags, note_id)
    )
    conn.commit()
    conn.close()


def delete_note(note_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()


def get_all_notes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_notes(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    pattern = f"%{keyword}%"
    cursor.execute(
        "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? OR category LIKE ? OR tags LIKE ? ORDER BY timestamp DESC",
        (pattern, pattern, pattern, pattern)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
