import sqlite3


def init_db(db_path):
    """
    Initialize the SQLite database and create the comparisons table if it does not exist.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        sqlite3.Connection: SQLite connection object.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comparisons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            image1_path TEXT,
            image2_path TEXT,
            diff_image_path TEXT,
            differences TEXT,
            width INTEGER,
            height INTEGER,
            parameters TEXT
        )
    ''')
    conn.commit()
    return conn


def insert_comparison_record(conn, record):
    """
    Insert a new comparison record into the database.

    Args:
        conn (sqlite3.Connection): The database connection object.
        record (dict): Dictionary containing comparison details.
    """
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO comparisons (
            timestamp, image1_path, image2_path, diff_image_path, differences, width, height, parameters
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        record['timestamp'],
        record['image1_path'],
        record['image2_path'],
        record['diff_image_path'],
        record['differences'],
        record['width'],
        record['height'],
        record['parameters']
    ))
    conn.commit()
