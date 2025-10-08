from datetime import datetime
from database import get_db

class Note:
    def __init__(self, id=None, title='', content='', created=None, updated=None, categories='', tags=''):
        self.id = id
        self.title = title
        self.content = content
        self.created = created
        self.updated = updated
        self.categories = categories  # Comma-separated if multiple
        self.tags = tags  # Comma-separated if multiple

    @staticmethod
    def create(title, content, categories='', tags=''):
        db = get_db()
        query = '''
        INSERT INTO notes (title, content, categories, tags) VALUES (?, ?, ?, ?)
        '''
        db.execute(query, (title, content, categories, tags))

    @staticmethod
    def update(note_id, title, content, categories='', tags=''):
        db = get_db()
        query = '''
        UPDATE notes
        SET title = ?, content = ?, categories = ?, tags = ?, updated = CURRENT_TIMESTAMP
        WHERE id = ?
        '''
        db.execute(query, (title, content, categories, tags, note_id))

    @staticmethod
    def delete(note_id):
        db = get_db()
        query = 'DELETE FROM notes WHERE id = ?'
        db.execute(query, (note_id,))

    @staticmethod
    def get_by_id(note_id):
        db = get_db()
        query = 'SELECT * FROM notes WHERE id = ?'
        rows = db.query(query, (note_id,))
        if rows:
            row = rows[0]
            return Note(
                id=row['id'], 
                title=row['title'],
                content=row['content'],
                created=row['created'],
                updated=row['updated'],
                categories=row['categories'],
                tags=row['tags']
            )
        return None

    @staticmethod
    def get_all():
        db = get_db()
        query = 'SELECT * FROM notes ORDER BY created DESC'
        rows = db.query(query)
        notes = []
        for row in rows:
            notes.append(Note(
                id=row['id'], 
                title=row['title'],
                content=row['content'],
                created=row['created'],
                updated=row['updated'],
                categories=row['categories'],
                tags=row['tags']
            ))
        return notes

    @staticmethod
    def search(keyword):
        db = get_db()
        # Search in title, content, categories, and tags
        pattern = f'%{keyword}%'
        query = '''
        SELECT * FROM notes WHERE 
          title LIKE ? OR 
          content LIKE ? OR 
          categories LIKE ? OR 
          tags LIKE ?
        ORDER BY created DESC
        '''
        rows = db.query(query, (pattern, pattern, pattern, pattern))
        notes = []
        for row in rows:
            notes.append(Note(
                id=row['id'], 
                title=row['title'],
                content=row['content'],
                created=row['created'],
                updated=row['updated'],
                categories=row['categories'],
                tags=row['tags']
            ))
        return notes
