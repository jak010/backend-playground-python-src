from __future__ import annotations

from abc import ABCMeta
from typing import Generic, TypeVar

from dependency_injector.wiring import Provide
from sqlalchemy.orm import Session

from src.domain.entity import MemberAggregate, MemberEntity, MemberProfileEntity
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

    def find_by_member_id(self, member_id: str) -> MemberEntity:
        """ One Table Querying """
        query = self.session.query(MemberEntity) \
            .filter(MemberEntity.nanoid == member_id)
        query = query.one_or_none()

        self.session.commit()
        return query

        # if query:
        #     aggregate = MemberAggregate.new(
        #         root_entitiy=query,
        #         member_profile=query.member_profile
        #     )
        #     return aggregate


class MemberProfileRepository(Repository):

    def save(self, member_profile_entity: MemberProfileEntity):
        self.session.add(member_profile_entity)
        self.session.commit()
        self.session.close()
