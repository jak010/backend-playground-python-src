from .repository.member_rdb_repository import MemberRDBRepository
from config.container import DataBaseContainer
from dependency_injector.wiring import Provide


class MemberService:
    member_repository = MemberRDBRepository()

    async def call(self):
        print(self.member_repository.find_by_id(member_id='asd'))
