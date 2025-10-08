import sqlite3

class NoteDatabase:
    def __init__(self, db_name="notes.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        query = '''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        '''
        cursor.execute(query)
        self.conn.commit()

    def add_note(self, title, content, timestamp):
        cursor = self.conn.cursor()
        query = "INSERT INTO notes (title, content, timestamp) VALUES (?, ?, ?)"
        cursor.execute(query, (title, content, timestamp))
        self.conn.commit()

    def update_note(self, note_id, title, content, timestamp):
        cursor = self.conn.cursor()
        query = "UPDATE notes SET title = ?, content = ?, timestamp = ? WHERE id = ?"
        cursor.execute(query, (title, content, timestamp, note_id))
        self.conn.commit()

    def delete_note(self, note_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM notes WHERE id = ?"
        cursor.execute(query, (note_id,))
        self.conn.commit()

    def get_notes(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM notes ORDER BY timestamp DESC"
        cursor.execute(query)
        return cursor.fetchall()

    def close(self):
        self.conn.close()
