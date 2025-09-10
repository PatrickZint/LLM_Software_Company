import sqlite3
import os

import config

_DB_CONN = None


def initialize_db():
    cfg = config.get_config()
    db_name = cfg.get('database', {}).get('name', 'file_organizer.db')
    conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source_path TEXT NOT NULL,
            destination_path TEXT NOT NULL,
            rule_applied TEXT
        )
    ''')
    conn.commit()
    global _DB_CONN
    _DB_CONN = conn


def get_db_connection():
    global _DB_CONN
    if _DB_CONN is None:
        initialize_db()
    return _DB_CONN


def log_operation(timestamp, source_path, destination_path, rule_applied):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO file_logs (timestamp, source_path, destination_path, rule_applied) 
            VALUES (?, ?, ?, ?)
        ''', (timestamp, source_path, destination_path, rule_applied))
        conn.commit()
    except Exception as e:
        print(f"Failed to log operation: {e}")


def get_all_logs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, source_path, destination_path, rule_applied FROM file_logs ORDER BY id DESC")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        return []
