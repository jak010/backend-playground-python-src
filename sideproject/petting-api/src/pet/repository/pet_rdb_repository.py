from __future__ import annotations

from typing import Optional, List

from sqlalchemy.exc import IntegrityError

from libs.abstract.abstract_rdb_repository import AbstracrtRDBRepository
from src.pet.entity import PetEntity, PetAttachmentEntity
from src.pet.enums import PetAttachmentType, PetAttachmentLabel
from .exception import PetEntityDuplicateException
from .interface import IPetRepository


class PetRDBRepository(AbstracrtRDBRepository, IPetRepository):
    def add(self, pet_entity: PetEntity) -> PetEntity:

        try:
            self.session.add(pet_entity)
            self.session.flush()
        except IntegrityError as e:
            self.session.rollback()
            raise PetEntityDuplicateException() from e

        return pet_entity

    def find_pet_by_pet_id(self, nanoid: str) -> Optional[PetEntity]:
        query = self.session.query(PetEntity).filter(PetEntity.nanoid == nanoid)
        query = query.one_or_none()
        if query:
            return query

    def find_pet_by_member(self, member_id: str) -> List[PetEntity]:
        """ 2024.04.21, 현재는 사용자가 하나의 Pet만 소유할 수 있게 처리되어있음 """
        query = self.session.query(PetEntity).filter(PetEntity.owner == member_id)
        return query.all()

    def find_pet_primary(self, member_id: str) -> PetEntity:
        """ 2024.04.21, Primary로 설정된 Pet 가져오기 """
        query = self.session.query(PetEntity) \
            .filter(PetEntity.owner == member_id) \
            .filter(PetAttachmentEntity.attachment_type == PetAttachmentType.PRIMARY.value) \
            .filter(PetAttachmentEntity.attachment_label == PetAttachmentLabel.PET.value)
        return query.one_or_none()
