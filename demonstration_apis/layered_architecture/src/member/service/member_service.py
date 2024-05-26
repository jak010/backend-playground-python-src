from src.member.repository import MemberRepository
from library.transactional import Transactional

from src.member.service.exceptions import (
    MemberNotFound,
    AlreadyExistMember
)

from external_library.orm import Member


class MemberService:
    member_repository = MemberRepository()

    @Transactional
    def get_member(self, member_id: int):
        member = self.member_repository.find_by_id(member_id=member_id)
        if member is None:
            raise MemberNotFound()

        return member

    @Transactional
    def register(self, name: str, age: int):
        member = self.member_repository.find_by_name(name=name)
        if member:
            raise AlreadyExistMember()

        self.member_repository.add(
            Member(name=name, age=age)
        )
