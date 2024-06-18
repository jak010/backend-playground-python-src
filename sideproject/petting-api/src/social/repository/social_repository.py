from __future__ import annotations

from libs.abstract.abstract_rdb_repository import AbstracrtRDBRepository as _AbstracrtRDBRepository
from src.social.entity import SocialEntity
from src.pet.entity import PetEntity
from src.pet.entity import PetAttachmentEntity
from typing import List, Tuple, Optional
from src.pet.enums import PetAttachmentType, PetAttachmentLabel
from src.social.enums import SocialInviteRequestStatus


class SocialRDBRepository(_AbstracrtRDBRepository):

    def save(self, entity: SocialEntity):
        self.session.add(entity)
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def find_social_sender(self, sender: str) -> List[SocialEntity]:
        query = self.session.query(SocialEntity).filter(SocialEntity.sender == sender)
        query = query.all()

        return query

    def find_social_receiver(self, receiver: str) -> List[Tuple[SocialEntity, PetEntity, PetAttachmentEntity]]:
        """ receiver를 기준으로 요청받은 친구목록 리스트 조회 """
        query = self.session.query(SocialEntity, PetEntity, PetAttachmentEntity) \
            .outerjoin(PetEntity, PetEntity.owner == SocialEntity.sender) \
            .outerjoin(PetAttachmentEntity, PetAttachmentEntity.nanoid == PetEntity.nanoid) \
            .filter(SocialEntity.receiver == receiver) \
            .filter(PetAttachmentEntity.attachment_label == PetAttachmentLabel.PET.value) \
            .filter(PetAttachmentEntity.attachment_type == PetAttachmentType.PRIMARY.value) \
            .filter(SocialEntity.status == SocialInviteRequestStatus.WAIT.value)

        return query.all()

    def find_social_by_invited(self, sender: str, receiver: str) -> Optional[SocialEntity]:
        query = self.session.query(SocialEntity) \
            .filter(SocialEntity.sender == sender) \
            .filter(SocialEntity.receiver == receiver) \
            .filter(SocialEntity.status == SocialInviteRequestStatus.WAIT.value)

        query = query.one_or_none()
        if query:
            return query

    def find_social_by_approval(self, sender: str, receiver: str) -> Optional[SocialEntity]:
        query = self.session.query(SocialEntity) \
            .filter(SocialEntity.sender == sender) \
            .filter(SocialEntity.receiver == receiver) \
            .filter(SocialEntity.status == SocialInviteRequestStatus.APPROVAL.value)

        query = query.one_or_none()
        if query:
            return query

    def find_by_pk(self, pk: int) -> Optional[SocialEntity]:
        query = self.session.query(SocialEntity).filter(SocialEntity.pk == pk)
        return query.one_or_none()
