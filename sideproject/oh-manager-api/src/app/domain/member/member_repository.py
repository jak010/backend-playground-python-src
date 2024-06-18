from typing import Optional

from src.app.domain.member import MemberEntity
from src.app.domain.abstract import AbstractRepository


class MemberRepository(AbstractRepository[MemberEntity]):

    def add(self, member_entity: MemberEntity) -> MemberEntity:
        self.session.add(member_entity)
        return member_entity

    def get_by_email(self, email: str) -> Optional[MemberEntity]:
        query = self.session.query(MemberEntity) \
            .filter(MemberEntity.email == email) \
            .one_or_none()
        if query:
            return query

    def get_by_id(self, member_id: str) -> MemberEntity:
        query = self.session.query(MemberEntity) \
            .filter(MemberEntity.id == member_id) \
            .one_or_none()
        if query:
            return query
