import json
import os
from note import create_note_dict

class NoteManager:
    def __init__(self, data_file='notes.json'):
        self.data_file = data_file
        self.notes = []
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            except json.JSONDecodeError:
                self.notes = []
        else:
            self.notes = []

    def save_notes(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, indent=4)

    def get_all_notes(self):
        # Optionally sort notes by timestamp or title
        return sorted(self.notes, key=lambda note: note['timestamp'], reverse=True)

    def create_note(self, title, content, timestamp):
        note = create_note_dict(title, content, timestamp)
        self.notes.append(note)
        return note

    def edit_note(self, note_id, new_title, new_content, timestamp):
        for note in self.notes:
            if note['id'] == note_id:
                note['title'] = new_title
                note['content'] = new_content
                note['timestamp'] = timestamp
                return note
        return None

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note['id'] != note_id]
