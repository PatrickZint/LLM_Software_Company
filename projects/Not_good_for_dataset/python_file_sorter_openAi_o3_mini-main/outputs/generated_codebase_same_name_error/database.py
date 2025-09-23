import sqlite3
import os
import datetime


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn


def initialize_db(db_path):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_path TEXT NOT NULL,
            destination_path TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            sorting_rule TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")


def log_file_movement(original, destination, rule, db_path_override=None):
    # If db_path_override is provided use it, else open default db
    from config import load_config
    config = load_config() or {}
    db_path = db_path_override or config.get('database', {}).get('path', 'file_logs.db')
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO file_logs (original_path, destination_path, timestamp, sorting_rule)
        VALUES (?, ?, ?, ?)
    ''', (original, destination, timestamp, rule))
    conn.commit()
    conn.close()
    print(f"Logged movement of {original} -> {destination} using rule {rule}")
