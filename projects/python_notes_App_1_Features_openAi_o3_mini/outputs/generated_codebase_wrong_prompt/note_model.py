import sqlite3
import datetime
from db import DB_NAME


class Note:
    def __init__(self, id, title, content, created_at, updated_at):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(title, content):
        """
        Create a new note with the provided title and content. Required fields are validated in the UI.
        """
        now = datetime.datetime.now().isoformat()
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, content, now, now)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def get_all():
        """
        Retrieve all notes from the database.
        """
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, content, created_at, updated_at FROM notes")
        rows = cursor.fetchall()
        connection.close()
        return [Note(*row) for row in rows]

    @staticmethod
    def get_by_id(note_id):
        """
        Retrieve a note by its unique identifier.
        """
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        connection.close()
        if row:
            return Note(*row)
        return None

    @staticmethod
    def update(note_id, title, content):
        """
        Update the title and content of an existing note and refresh the updated_at timestamp.
        """
        now = datetime.datetime.now().isoformat()
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?",
            (title, content, now, note_id)
        )
        connection.commit()
        connection.close()

    @staticmethod
    def delete(note_id):
        """
        Delete a note from the database by its unique identifier.
        """
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        connection.commit()
        connection.close()