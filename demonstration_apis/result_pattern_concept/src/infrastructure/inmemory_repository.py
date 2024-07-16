import uuid
from typing import Optional, Dict
from src.contrib import errors


class InMemoryRepository:
    _storage = {
        "items": [
            {
                'id': 1,
                'content': str(uuid.uuid4())
            },
            {
                'id': 2,
                'content': "test"
            },
        ]
    }

    def find_by_id(self, id: int) -> Dict:
        for item in self._storage['items']:
            if item['id'] == id:
                return item

    def add(self, id: int, content: str):

        items = self._storage['items']
        for item in items:
            if content == item['content']:
                return False

        self._storage['items'].append(
            {
                "id": id,
                "content": content
            }
        )
