from __future__ import annotations

import datetime
from typing import TypeVar, Generic

from dependency_injector.wiring import Provide
from sqlalchemy.orm.session import Session

from settings.container.db_container import DataBaseContainer

T = TypeVar("T")


class AbstracrtRDBRepository:
    session: Session = Provide[DataBaseContainer.session]


class SQLAlchemySessionFactory:

    @staticmethod
    def get_session(): ...


class AbstractRDBRepository(Generic[T]):
    session: Session = SQLAlchemySessionFactory.get_session()

    def save(self) -> T: ...

    def get(self, id) -> T: ...


import dataclasses


@dataclasses.dataclass
class MemberEntity: ...


class MemberRepository(AbstractRDBRepository[MemberEntity]):

    def save(self) -> MemberEntity: ...

    def get(self, id) -> MemberEntity: ...
