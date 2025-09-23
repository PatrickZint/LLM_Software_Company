import unittest
import os
import json
from note import Note
from database import NoteDatabase
from exporter import export_notes, import_notes
from config import DB_PATH, EXPORT_PATH


class TestNoteDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use an in-memory database for testing
        cls.db = NoteDatabase(":memory:")

    def test_add_and_get_note(self):
        note = Note(title="Test Note", content="Content of test note", category="Test", tags="unit,test")
        inserted = self.db.add_note(note)
        self.assertIsNotNone(inserted.id)

        fetched = self.db.get_note_by_id(inserted.id)
        self.assertEqual(fetched.title, "Test Note")

    def test_update_note(self):
        note = Note(title="Original Title", content="Original Content")
        inserted = self.db.add_note(note)
        inserted.title = "Updated Title"
        self.db.update_note(inserted)
        updated = self.db.get_note_by_id(inserted.id)
        self.assertEqual(updated.title, "Updated Title")

    def test_delete_note(self):
        note = Note(title="To be deleted", content="Some content")
        inserted = self.db.add_note(note)
        self.db.delete_note(inserted.id)
        deleted = self.db.get_note_by_id(inserted.id)
        self.assertIsNone(deleted)

    def test_search_notes(self):
        note = Note(title="UniqueTitle123", content="Content")
        self.db.add_note(note)
        results = self.db.search_notes("UniqueTitle123")
        self.assertTrue(any(n.title == "UniqueTitle123" for n in results))


class TestExporter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = NoteDatabase(":memory:")
        cls.note = Note(title="Export Test", content="Export Content")
        cls.db.add_note(cls.note)
        cls.export_file = EXPORT_PATH

    def test_export_notes(self):
        notes = self.db.get_all_notes()
        export_notes(notes, self.export_file)
        self.assertTrue(os.path.exists(self.export_file))

    def test_import_notes(self):
        # First export a note
        notes = self.db.get_all_notes()
        export_notes(notes, self.export_file)
        # Now import
        imported = import_notes(self.export_file)
        self.assertGreaterEqual(len(imported), 1)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.export_file):
            os.remove(cls.export_file)


if __name__ == '__main__':
    unittest.main()
