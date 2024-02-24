from abc import ABCMeta
from typing import NoReturn

from notepad.structure.domain.i_xxx_repository import IXXXRepository
from notepad.structure.domain.model import MemberEntity

from sqlalchemy.orm.session import Session


class SQLAlchemyMemberRepository(IXXXRepository):
    session: Session = None

    @classmethod
    def find_by_id(cls, *args, **kwrags) -> MemberEntity:
        return cls.session.query(MemberEntity).all()

    @classmethod
    def save(cls, *args, **kwrags) -> NoReturn:
        pass
