import sqlite3

DB_NAME = 'habits.db'

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create table for habits
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS habit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        goal TEXT NOT NULL,
        schedule TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT,
        category TEXT
    )
    ''')

    # Create table for habit logs/completions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS habit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        log_date TEXT NOT NULL,
        status TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (habit_id) REFERENCES habit(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print('Database initialized.')
