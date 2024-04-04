from sqlalchemy.orm.session import Session

from .entity.member_entity import MemberEntity
from settings.abstracts import AbstracRDBRepository, IRepository


class MemberRepository(IRepository[MemberEntity]):

    def find_by_user_id(self, member_id):
        query = self.session.query(MemberEntity).filter(MemberEntity.pk == member_id)
        return query.one_or_none()

    def find_by_id(self) -> MemberEntity:
        ...
