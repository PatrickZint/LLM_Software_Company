import sqlite3


def init_db(db_path):
    """
    Initialize the SQLite database. If the notes table does not exist, create it.
    """
    conn = sqlite3.connect(db_path)
    create_table(conn)
    return conn


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()


def get_all_notes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, created_timestamp, updated_timestamp FROM notes ORDER BY created_timestamp DESC")
    return cursor.fetchall()


def get_note_by_id(conn, note_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, created_timestamp, updated_timestamp FROM notes WHERE id = ?", (note_id,))
    return cursor.fetchone()


def create_note(conn, title, content):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    return cursor.lastrowid


def update_note(conn, note_id, title, content):
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title = ?, content = ?, updated_timestamp = CURRENT_TIMESTAMP WHERE id = ?",
                   (title, content, note_id))
    conn.commit()


def delete_note(conn, note_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
