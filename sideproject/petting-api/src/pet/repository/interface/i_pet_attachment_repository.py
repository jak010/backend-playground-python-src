from __future__ import annotations

from abc import abstractmethod, ABC

from src.pet.entity.pet_attachment_entity import PetAttachmentEntity


class IPetAttachmentRepository(ABC):

    @abstractmethod
    def add(self, pet_attachment_entity: PetAttachmentEntity) -> PetAttachmentEntity: ...

    @abstractmethod
    def find_by_member(self, member_id: str) -> PetAttachmentEntity: ...
