from src.libs.i_repository import IRepository, IRDBRepository

from ..entity import MemberEntity

from adapter.database.orm import Member


class MemberRDBRepository(IRDBRepository[MemberEntity]):

    def find_by_id(self, member_id: str):
        query = self.session.query(Member).all()
        self.session.commit()
        self.session.close()
