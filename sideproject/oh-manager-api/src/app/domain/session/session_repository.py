from __future__ import annotations

from typing import Optional

from src.app.domain.abstract import AbstractRepository
from src.app.domain.session.session_entity import SessionEntity


class SessionRepository(AbstractRepository[SessionEntity]):

    def get_by_session_id(self, session_id: str) -> Optional[SessionEntity]:
        query = self.session.query(SessionEntity) \
            .filter(SessionEntity.session_id == session_id)
        query = query.one_or_none()
        if query:
            return query

    def add(self, session_entity: SessionEntity) -> SessionEntity:
        self.session.add(session_entity)
        self.session.flush()
        return session_entity

    def delete(self, session_entity: SessionEntity) -> SessionEntity:
        self.session.delete(session_entity)
        self.session.flush()
        return session_entity
