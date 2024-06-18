from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.session import SessionEntity


class ISessionRepository(ABC):

    @abstractmethod
    def add(self, session_entity: SessionEntity) -> SessionEntity: ...

    @abstractmethod
    def find_session_by_nanoid(self, nanoid: str) -> SessionEntity: ...

    @abstractmethod
    def delete_session_by_nanoid(self, nanoid: str) -> SessionEntity: ...