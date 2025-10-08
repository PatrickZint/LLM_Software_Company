import json
import os
import db
import encryption
import tkinter as tk
from tkinter import filedialog, messagebox


def export_notes(user_id):
    notes = db.get_notes(user_id)
    # Prepare export data. Note: encrypted content is stored; export as base64 encoded string if needed
    export_data = []
    for note in notes:
        export_data.append({
            'id': note['id'],
            'title': note['title'],
            'content': note['content'].decode('utf-8') if isinstance(note['content'], bytes) else note['content'],
            'timestamp': note['timestamp'],
            'tags': note['tags'],
            'categories': note['categories']
        })
    
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension='.json',
        filetypes=[('JSON Files', '*.json')],
        title='Export Notes')
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4)
            messagebox.showinfo('Export', 'Notes exported successfully.')
        except Exception as e:
            messagebox.showerror('Export Error', str(e))
    root.destroy()


def import_notes(user_id, file_path, encryption_key):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Validate schema
        for note in data:
            if not all(k in note for k in ('title', 'content', 'timestamp')):
                return False
            # Re-encrypt the content before storing
            encrypted_content = encryption.encrypt_data(encryption_key, note['content'])
            tags = note.get('tags', '')
            categories = note.get('categories', '')
            db.add_note(user_id, note['title'], encrypted_content, note['timestamp'], tags, categories)
        return True
    except Exception as e:
        print('Import error:', e)
        return False
