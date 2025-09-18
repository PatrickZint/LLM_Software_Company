import sqlite3
import os

# Database filename
DB_NAME = 'notes.db'


def init_db():
    """
    Initialize the SQLite database and create the necessary tables if they do not already exist.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    
    # Create the notes table with required fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


if __name__ == '__main__':
    init_db()
    print("Database initialized.")