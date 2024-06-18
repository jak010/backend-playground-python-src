from __future__ import annotations

from typing import NoReturn, List

from libs.abstract.abstract_rdb_repository import AbstracrtRDBRepository
from src.session.entity import SessionEntity
from src.session.repository.interface import ISessionRepository
from .exception import SessionDoesNotExistException


class SessionRDBRepository(AbstracrtRDBRepository, ISessionRepository):

    def add(self, session_entity: SessionEntity) -> SessionEntity:
        self.session.add(session_entity)
        self.session.flush()
        return session_entity

    def find_session_by_nanoid(self, nanoid: str) -> SessionEntity:
        query = self.session.query(SessionEntity).filter_by(nanoid=nanoid).one_or_none()
        if query:
            return query

    def find_session_by_member_id(self, member_id: str) -> List[SessionEntity]:
        query = self.session.query(SessionEntity) \
            .filter(SessionEntity.member_id == member_id)
        return query.all()

    def delete_session_by_nanoid(self, nanoid: str):
        query = self.session.query(SessionEntity) \
            .filter(SessionEntity.nanoid == nanoid) \
            .one_or_none()

        if query:
            self.session.delete(query)
            self.session.flush(query)
        raise SessionDoesNotExistException()

    def delete_session_by_member_id(self, member_id: str) -> NoReturn:
        self.session.query(SessionEntity). \
            filter(SessionEntity.member_id == member_id) \
            .delete()
        self.session.flush()
