import uuid

def create_note_dict(title, content, timestamp, note_id=None):
    """
    Helper function to create a note dictionary.
    If note_id is not provided, a new unique id is generated.
    """
    return {
        'id': note_id if note_id is not None else str(uuid.uuid4()),
        'title': title,
        'content': content,
        'timestamp': timestamp
    }
