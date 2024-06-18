from __future__ import annotations

from tempfile import NamedTemporaryFile

from fastapi import UploadFile

from libs.abstract.abstract_usecase import AbstractUseCase
from settings.policy.define import (
    PET_IMAGE_PRIMARY_LIMIT,
    PET_SELFIE_IMAGE_PRIMARY_LIMIT
)
from src.member.repository import MemberAssetRDBRepository, MemberRDBRepository
from src.member.service import MemberAssetService, MemberService
from src.pet.entity.pet_attachment_entity import PetAttachmentEntity
from src.pet.repository import (
    PetAttachmentRDBRepository,
    PetRDBRepository, PetAttachmnetEntityDuplicateException
)
from src.pet.enums import (
    PetAttachmentType,
    PetAttachmentLabel
)
from src.session.entity import SessionEntity
from .exceptions import (
    PetUploadFileAlreadySetPrimaryException,
    NotExistPetEntityException,
    MaxUploadImageLimitException, PetUploadFileDuplicateException
)
from .pet_s3_storage import PetImageStorage

from src.member.events.member_issued_coin_event import MemberIssuedCoinWhenImageUploadedEvent

from dependency_injector.wiring import Provide
from settings.container.event_container import EventContainer, EventHandler


class AbstractPetImageUpdateUseCase(AbstractUseCase):
    pet_image_storage = PetImageStorage()

    pet_repository = PetRDBRepository()
    pet_attachment_repository = PetAttachmentRDBRepository()

    member_asset_repository = MemberAssetRDBRepository()
    member_asset_service = MemberAssetService()

    member_repository = MemberRDBRepository()
    member_service = MemberService()


class PetImageUploadUseCase(AbstractPetImageUpdateUseCase):
    MAX_UPLOAD_IMAGE_LIMIT = 10
    ASSET_ISSUED_QUANTITY = 2

    event_handler: EventHandler = Provide[EventContainer.handler]

    async def execute(
            self,
            owner: SessionEntity,
            pet_id: str,
            attachment_type: str,
            attachment_label: str,
            file: UploadFile
    ):
        pet = await self._find_pet(pet_id)
        pet_attachment = await self._insert_attachment(attachment_label, attachment_type, file, owner, pet)

        await self._validate_image_upload_limit(attachment_label, owner)
        await self._validate_image_primary_limit(attachment_label, attachment_type)

        # AWS S3, Image Upload
        with NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(await file.read())

            s3_key = self.pet_image_storage.upload_pets_image(
                owner=owner.member,
                upload_name=f"{pet.name}_{file.filename}",
                content_type=file.content_type,
                attachment_label=attachment_label,
                file=temp_file
            )

            pet_attachment.s3_key = s3_key
            self.pet_attachment_repository.add(pet_attachment)

        self.event_handler.add_event(
            MemberIssuedCoinWhenImageUploadedEvent(owner)
        )

    async def _find_pet(self, pet_id):
        pet = self.pet_repository.find_pet_by_pet_id(nanoid=pet_id)
        if pet is None:
            raise NotExistPetEntityException()
        return pet

    async def _insert_attachment(self, attachment_label, attachment_type, file, owner, pet):
        from libs.utils import file_utils

        try:
            pet_attachment = self.pet_attachment_repository.add(
                pet_attachment_entity=PetAttachmentEntity.new(
                    nanoid=pet.nanoid,
                    member_id=owner.member_id,
                    attachment_type=PetAttachmentType.to(attachment_type),
                    attachment_label=PetAttachmentLabel.to(attachment_label),
                    s3_key=None,
                    file_name=file_utils.normailize_file_name(file.filename),
                    content_type=file.content_type,
                    file_size=file.size
                ))
        except PetAttachmnetEntityDuplicateException:
            raise PetUploadFileDuplicateException()

        return pet_attachment

    async def _validate_image_upload_limit(self, attachment_label, owner):
        """   pet image 업로드 제한 """
        pet_attahcments_type_with_label_count = self.pet_attachment_repository.get_pet_attachment_type_label_count(
            member_id=owner.member_id,
            attachment_label=attachment_label
        )

        if pet_attahcments_type_with_label_count >= self.MAX_UPLOAD_IMAGE_LIMIT:
            raise MaxUploadImageLimitException()

    async def _validate_image_primary_limit(self, attachment_label, attachment_type):
        """ pet image 업로드 제한: 각 type 별 대표 사진은 2장씩만 등록 가능 """
        primary_counts = self.pet_attachment_repository.find_by_pet_attachment_primary_aggregate()
        if attachment_type == PetAttachmentType.PRIMARY.value:
            if attachment_label == PetAttachmentLabel.PET.value and \
                    primary_counts[PetAttachmentLabel.PET.value] > PET_IMAGE_PRIMARY_LIMIT:
                raise PetUploadFileAlreadySetPrimaryException()
            if attachment_label == PetAttachmentLabel.SELFIE.value and \
                    primary_counts[PetAttachmentLabel.SELFIE.value] > PET_SELFIE_IMAGE_PRIMARY_LIMIT:
                raise PetUploadFileAlreadySetPrimaryException()
