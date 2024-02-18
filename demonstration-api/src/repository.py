from functools import cached_property
from typing import Protocol, Generic, TypeVar

from dependency_injector.wiring import Provide, Closing, inject
from sqlalchemy.orm import Session

from settings.dependency import DataBaseContainer

Entity = TypeVar("Entity")


class IRepository(Generic[Entity], Protocol):
    session = Provide[DataBaseContainer.session]
    # @cached_property
    # @inject
    # def session(self, _session: Session = Closing[Provide[DataBaseContainer.session]]):
    #     return _session


class Repository(IRepository):

    def get_session(self):
        self.session.execute("select 1;")
        self.session.commit()
        self.session.close()
