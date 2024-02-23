from __future__ import annotations

from abc import ABCMeta
from typing import Generic, TypeVar

from dependency_injector.wiring import Provide
from sqlalchemy.orm import Session

from core.entity.member_entity import MemberEntity
from core.entity.member_profile_entity import MemberProfileEntity
from settings.dependency import DataBaseContainer

Entity = TypeVar("Entity")


class IRepository(Generic[Entity], metaclass=ABCMeta):
    session: Session = Provide[DataBaseContainer.session]


class Repository(IRepository):

    def get_session(self):
        self.session.execute("select 1;")
        self.session.commit()
        self.session.close()


class MemberRepositry(Repository):

    def save(self, member_entity: MemberEntity):
        self.session.add(member_entity)
        self.session.commit()
        self.session.close()

    def get(self, member_id: str):
        """ One Table Querying """
        query = self.session.query(MemberEntity) \
            .filter(MemberEntity.member_id == nanoid)
        query = query.one_or_none()

        if query:
            return query


class MemberProfileRepository(Repository):

    def save(self, member_profile_entity: MemberProfileEntity):
        self.session.add(member_profile_entity)
        self.session.commit()
        self.session.close()
