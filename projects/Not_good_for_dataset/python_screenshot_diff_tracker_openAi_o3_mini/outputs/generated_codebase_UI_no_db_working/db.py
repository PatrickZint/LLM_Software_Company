import sqlite3
import os
from datetime import datetime

DB_FILENAME = 'image_diff_logs.db'


def init_db(db_path=DB_FILENAME):
    """
    Initialize the SQLite database for logging image comparisons
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comparisons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image1_path TEXT,
            image2_path TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()


def log_comparison(image1_path, image2_path, db_path=DB_FILENAME):
    """
    Log the comparison event in the SQLite database
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO comparisons (image1_path, image2_path, timestamp) VALUES (?, ?, ?)',
                   (image1_path, image2_path, timestamp))
    conn.commit()
    conn.close()


# If running this module directly, initialize the database
if __name__ == '__main__':
    init_db()
    print(f'Database initialized and stored in {DB_FILENAME}')
