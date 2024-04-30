from typing import Generic, TypeVar, NoReturn, Protocol

from dependency_injector.wiring import Provide
from sqlalchemy.orm.session import Session

from config.container import DataBaseContainer

T = TypeVar("T")


class IRepository(Protocol):

    def find_by_id(self, member_id: str) -> T: ...

    def delete_by_id(self, member_id: str) -> NoReturn: ...


class IRDBRepository(IRepository, Generic[T]):
    db_client = Provide[DataBaseContainer.db_client]

    @property
    def session(self) -> Session:
        return self.db_client.get_session()
