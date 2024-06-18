from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from src.pet.entity.pet_entity import PetEntity


class IPetRepository(ABC):

    @abstractmethod
    def add(self, pet_entity: PetEntity) -> PetEntity: ...

    @abstractmethod
    def find_pet_by_pet_id(self, nanoid: str) -> Optional[PetEntity]: ...

    @abstractmethod
    def find_pet_by_member(self, member_id: str) -> PetEntity: ...
