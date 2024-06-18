import abc
import dataclasses
from typing import Optional, Generic, TypeVar, Tuple, List, ClassVar

from dependency_injector.wiring import Provide
from sqlalchemy.orm import Session

from src.config.container.database_container import DataBaseContainer

Entity = TypeVar("Entity")


@dataclasses.dataclass
class AbstractDomainEntity:
    id: Optional[int] = dataclasses.field(default=None)

    def to_dict(self):
        return {k: str(v) for k, v in dataclasses.asdict(self).items()}

    def read(self, exclude_fields: list):
        data = self.to_dict()
        for field in exclude_fields:
            data.pop(field)
        return data


class AbstractRepository(Generic[Entity], metaclass=abc.ABCMeta):
    session: Session = Provide[DataBaseContainer.session]

    def get_by(self, *args, **kwargs) -> Tuple[List[Entity], int]: ...

    def get_by_id(self, *args, **kwargs) -> Optional[Entity]: ...

    def add(self, entity: Entity) -> Entity: ...

    def update(self, *args, **kwargs) -> Entity: ...

    def delete(self, entity: Entity) -> Entity: ...


class AbstractCommandQuery(metaclass=abc.ABCMeta):
    session: Session = Provide[DataBaseContainer.session]
