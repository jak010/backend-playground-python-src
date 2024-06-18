from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.member import MemberEntity


class IMemberRepository(ABC):

    @abstractmethod
    def add(self, member_entity: MemberEntity) -> MemberEntity: ...

    @abstractmethod
    def find_member_by_nanoid(self, nanoid: str) -> MemberEntity: ...
