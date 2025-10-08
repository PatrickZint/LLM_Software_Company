'''Models module: Defines User and Note data structures'''


class User:
    def __init__(self, id, username, password_hash, salt):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.salt = salt


class Note:
    def __init__(self, id, user_id, title, content, timestamp, tags=None, categories=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.timestamp = timestamp
        self.tags = tags
        self.categories = categories
