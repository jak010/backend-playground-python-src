from typing import Union

from libs.abstract.event_dispatcher import AbstractEvent
from settings.policy.define import PET_IMAGE_PRIMARY_LIMIT, PET_SELFIE_IMAGE_PRIMARY_LIMIT
from src.member.entity import MemberAssetEntity
from src.member.entity import MemberEntity
from src.member.enums import MemberAssetType
from src.member.repository import MemberAssetRDBRepository
from src.pet.enums import PetAttachmentLabel
from src.pet.repository import PetAttachmentRDBRepository
from src.session.entity import SessionEntity


class MemberIssuedCoinWhenImageUploadedEvent(AbstractEvent):
    REASON = "IMAGE_UPLOAD_COMPLETE_EVENT"
    ISSUED_COIN_QUANTITY = 2

    member_asset_repository = MemberAssetRDBRepository()
    pet_attachment_repository = PetAttachmentRDBRepository()

    def __init__(self, member):
        self.member: Union[MemberEntity, SessionEntity] = member

    def publish(self):
        primary_counts = self.pet_attachment_repository.find_by_pet_attachment_primary_aggregate()

        if self.check_primary_image_limits(primary_counts):
            member_asset = self.member_asset_repository.find_member_asset_by_image_upload_event(
                member_id=self.member.member_id,
                reason=self.REASON
            )
            if not member_asset:
                member_asset = MemberAssetEntity.new(
                    member_id=self.member.member_id,
                    issued_quantity=self.ISSUED_COIN_QUANTITY,
                    reason=self.REASON,
                    type=MemberAssetType.COIN
                )
                self.member_asset_repository.add(member_asset)
                return member_asset

    @classmethod
    def check_primary_image_limits(cls, primary_counts):
        """ PET & SELFIE는 각각 2개 이상의 대표(Primary) 사진 개수 체크  """
        return primary_counts[PetAttachmentLabel.PET.value] >= PET_IMAGE_PRIMARY_LIMIT and \
            primary_counts[PetAttachmentLabel.SELFIE.value] >= PET_SELFIE_IMAGE_PRIMARY_LIMIT
