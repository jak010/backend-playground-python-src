from sqlalchemy.orm import Session
from typing import Optional
from library.abstract import AbstractRdbRepsitory

from external_library.orm import Member


class MemberRepository(AbstractRdbRepsitory[Member]):

    def add(self, model: Member):
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        return self.session

    def find_by_id(self, member_id: int) -> Optional[Member]:
        return self.session.query(Member).filter(Member.pk == member_id).one_or_none()

    def find_by_name(self, name: str) -> Optional[Member]:
        return self.session.query(Member) \
            .filter(Member.name == name) \
            .one_or_none()

    def get_member(self):
        r = self.session.query(Member).one_or_none()
        return r
