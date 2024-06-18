from __future__ import annotations

from typing import Optional, List

from sqlalchemy import func, exc

from libs.abstract.abstract_rdb_repository import AbstracrtRDBRepository
from src.pet.entity import PetAttachmentEntity
from src.pet.enums import PetAttachmentType, PetAttachmentLabel
from .interface import IPetAttachmentRepository
from .exception import PetAttachmnetEntityDuplicateException


class PetAttachmentRDBRepository(AbstracrtRDBRepository, IPetAttachmentRepository):
    def add(self, pet_attachment_entity: PetAttachmentEntity) -> PetAttachmentEntity:
        try:
            self.session.add(pet_attachment_entity)
            self.session.flush()
        except exc.IntegrityError:
            raise PetAttachmnetEntityDuplicateException()

        return pet_attachment_entity

    def find_by_member(self, member_id: str) -> Optional[List[PetAttachmentEntity]]:
        query = self.session.query(PetAttachmentEntity).filter(PetAttachmentEntity.member_id == member_id)
        return query.all()

    def get_pet_attachment_type_label_count(
            self,
            member_id: str,
            attachment_label: str
    ) -> int:
        return self.session.query(PetAttachmentEntity) \
            .filter(PetAttachmentEntity.member_id == member_id) \
            .filter(PetAttachmentEntity.attachment_label == attachment_label) \
            .count()

    def find_by_pet_attachment_primary_aggregate(self):
        query = self.session.query(PetAttachmentEntity.attachment_label,
                                   func.count(PetAttachmentEntity.attachment_type)) \
            .filter(PetAttachmentEntity.attachment_type == PetAttachmentType.PRIMARY.value) \
            .group_by(PetAttachmentEntity.attachment_label)

        primary_count = {
            PetAttachmentLabel.PET.value: 0,
            PetAttachmentLabel.SELFIE.value: 0
        }
        for label, count in query.all():
            if label == PetAttachmentLabel.PET.value:
                primary_count[PetAttachmentLabel.PET.value] = count
            if label == PetAttachmentLabel.SELFIE.value:
                primary_count[PetAttachmentLabel.SELFIE.value] = count

        return primary_count

    def find_pet_attachment_by_primary(self, member_id: str, pet_nano_id: str) -> PetAttachmentEntity:
        query = self.session.query(PetAttachmentEntity) \
            .filter(PetAttachmentEntity.attachment_type == PetAttachmentType.PRIMARY.value) \
            .filter(PetAttachmentEntity.attachment_label == PetAttachmentLabel.PET.value) \
            .filter(PetAttachmentEntity.member_id == member_id) \
            .filter(PetAttachmentEntity.nanoid == pet_nano_id)
        return query.one_or_none()
