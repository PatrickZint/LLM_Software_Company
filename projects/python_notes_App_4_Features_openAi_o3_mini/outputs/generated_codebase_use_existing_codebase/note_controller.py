from note_dao import NoteDAO
from data_io import import_notes_json, export_notes_json


class NoteController:
    def __init__(self):
        self.dao = NoteDAO()

    def get_all_notes(self):
        # Return a list of note dictionaries
        return self.dao.get_all_notes()

    def create_note(self, title, content, categories=None, tags=None):
        note = {
            'title': title,
            'content': content,
            'categories': categories or [],
            'tags': tags or []
        }
        return self.dao.create_note(note)

    def update_note(self, note_id, title=None, content=None, categories=None, tags=None):
        note = self.dao.get_note(note_id)
        if not note:
            return None
        if title is not None:
            note['title'] = title
        if content is not None:
            note['content'] = content
        if categories is not None:
            note['categories'] = categories
        if tags is not None:
            note['tags'] = tags
        self.dao.update_note(note_id, note)
        return note

    def delete_note(self, note_id):
        self.dao.delete_note(note_id)

    def export_notes(self, filepath):
        notes = self.dao.get_all_notes()
        return export_notes_json(notes, filepath)

    def import_notes(self, filepath):
        notes = import_notes_json(filepath)
        if notes is None:
            return False
        for note in notes:
            self.dao.create_note(note)
        return True
