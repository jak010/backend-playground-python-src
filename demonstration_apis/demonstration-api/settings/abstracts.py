from sqlalchemy.orm.session import Session

from sqlalchemy.orm.session import Session

from dependency_injector.wiring import Provide

from settings.dependency import DataBaseContainer
from settings.ioc import IocContainer

from typing import Generic, TypeVar

T = TypeVar("T")
Entity = TypeVar("Entity")


class AbstracRDBRepository(Generic[T]):
    session: Session = Provide[IocContainer.session]

    def find_by_id(self) -> T: ...


class IRepository(Generic[Entity]):
    session: Session = Provide[DataBaseContainer.session]

    def add(self, entity: Entity) -> T:
        self.session.add(entity)
        self.session.flush()
        self.session.refresh(entity)
        self.session.commit()
        self.session.close()
        return entity

    def find_by_id(self) -> T: ...
