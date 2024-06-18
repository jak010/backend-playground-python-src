from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.member.entity import MemberProfileEntity


class IMemberProfileRepository(ABC):

    @abstractmethod
    def add(self, member_profile_entity: MemberProfileEntity) -> MemberProfileEntity: ...

    @abstractmethod
    def find_member_profile_by_nanoid(self, nanoid: str) -> MemberProfileEntity: ...
