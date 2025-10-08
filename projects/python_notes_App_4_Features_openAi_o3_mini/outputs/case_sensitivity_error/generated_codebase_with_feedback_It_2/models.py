from dataclasses import dataclass
from typing import Optional


@dataclass
class Note:
    id: Optional[int]  # Will be None for new notes
    title: str
    content: str
    created_at: str
    updated_at: str
    categories: str  # Comma separated string of categories
    tags: str        # Comma separated string of tags

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'categories': self.categories,
            'tags': self.tags
        }

    @staticmethod
    def from_dict(data: dict):
        return Note(
            id=data.get('id'),
            title=data.get('title', ''),
            content=data.get('content', ''),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', ''),
            categories=data.get('categories', ''),
            tags=data.get('tags', '')
        )
