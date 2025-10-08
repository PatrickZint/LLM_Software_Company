import sqlite3
import os
import json

# Load configuration
CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as cf:
        config = json.load(cf)
else:
    config = {}

DB_PATH = config.get('DatabaseFilePath', 'notes.db')

# Ensure the folder for the database exists
os.makedirs(os.path.dirname(DB_PATH) or '.', exist_ok=True)


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        query = '''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            categories TEXT,
            tags TEXT
        );
        '''
        self.connection.execute(query)
        self.connection.commit()

    def execute(self, query, params=()):
        cur = self.connection.cursor()
        cur.execute(query, params)
        self.connection.commit()
        return cur

    def query(self, query, params=()):
        cur = self.connection.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return rows

    def close(self):
        self.connection.close()


# Singleton style instance for usage across modules
_db_instance = None

def get_db():
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
