from typing import Protocol, Generic, TypeVar, List
from dependency_injector.wiring import Provide
from settings.dependency import DataBaseContainer
from functools import cached_property
from sqlalchemy.orm import Session

Entity = TypeVar("Entity")


class IRepository(Generic[Entity], Protocol):

    def get_all(self, *args, **kwargs) -> List[Entity]:
        raise NotImplementedError()

    def get(self, *args, **kwargs) -> Entity:
        raise NotImplementedError()


class Repository(IRepository):
    session: Session = Provide[DataBaseContainer.session]

    def get_session(self):
        self.session.execute("select 1;")
        self.session.commit()

