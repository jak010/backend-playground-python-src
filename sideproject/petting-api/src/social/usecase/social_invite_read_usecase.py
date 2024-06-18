from libs.abstract.abstract_usecase import AbstractUseCase

from src.session.entity import SessionEntity
from src.social.controller.request import SocialInviteRequestDto
from typing import List, Tuple
from src.member.repository import MemberRDBRepository
from src.social.repository import SocialRDBRepository
from src.social.service import SocialService
from src.social.entity import SocialEntity
from src.pet.entity import PetEntity, PetAttachmentEntity

from src.social.controller.request.social_invite_dto import SocialInviteDto, SocialInviteList


class SocialInviteReadUsecase(AbstractUseCase):
    """ 친구 요청 받은 목록 보기 """

    def __init__(self):
        self.social_repository = SocialRDBRepository()
        self.social_service = SocialService()

        self.member_repository = MemberRDBRepository()

    def execute(self, session: SessionEntity) -> SocialInviteList:
        socials = self.social_repository.find_social_receiver(receiver=session.member_id)

        return SocialInviteList(
            count=len(socials),
            items=[
                SocialInviteDto(
                    social_id=social.pk,
                    member_id=social.sender,
                    pet_name=pet.name,
                    pet_breed=pet.breed,
                    pet_pdit=pet.pdti,
                    pet_pdit_type=pet.pdti_type,
                    pet_image=pet_attachment.s3_key,
                    invited_time=social.created_at.isoformat())
                for social, pet, pet_attachment in socials
            ])
