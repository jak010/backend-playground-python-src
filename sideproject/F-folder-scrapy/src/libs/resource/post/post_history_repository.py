from __future__ import annotations

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.post.post_history_entity import PostHistoryEntity


class PostHistoryRepository(AbstractRepository):
    def add(self, post_history_entity: PostHistoryEntity):
        self._session.add(post_history_entity)
        self._session.flush()
