import sqlite3
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Create Habits table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            schedule_type TEXT NOT NULL,  -- daily or weekly
            goal TEXT,
            expected_frequency INTEGER,
            start_date TEXT NOT NULL,
            end_date TEXT
        );
    ''')
    # Create Completions table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
        );
    ''')
    conn.commit()
    conn.close()


def add_habit(name, description, schedule_type, goal, expected_frequency, start_date, end_date=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO habits (name, description, schedule_type, goal, expected_frequency, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, description, schedule_type, goal, expected_frequency, start_date, end_date))
    conn.commit()
    habit_id = cur.lastrowid
    conn.close()
    return habit_id


def update_habit(habit_id, name, description, schedule_type, goal, expected_frequency, start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE habits
        SET name=?, description=?, schedule_type=?, goal=?, expected_frequency=?, start_date=?, end_date=?
        WHERE id=?
    ''', (name, description, schedule_type, goal, expected_frequency, start_date, end_date, habit_id))
    conn.commit()
    conn.close()


def delete_habit(habit_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM habits WHERE id=?', (habit_id,))
    conn.commit()
    conn.close()


def get_all_habits():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM habits')
    rows = cur.fetchall()
    conn.close()
    return rows


def add_completion(habit_id, date, timestamp):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO completions (habit_id, date, timestamp)
        VALUES (?, ?, ?)
    ''', (habit_id, date, timestamp))
    conn.commit()
    conn.close()


def get_completions_for_habit(habit_id, start_date=None, end_date=None):
    conn = get_connection()
    cur = conn.cursor()
    query = 'SELECT * FROM completions WHERE habit_id=?'
    params = [habit_id]
    if start_date:
        query += ' AND date >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND date <= ?'
        params.append(end_date)
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return rows
