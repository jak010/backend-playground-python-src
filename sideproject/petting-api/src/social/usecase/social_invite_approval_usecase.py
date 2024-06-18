from libs.abstract.abstract_usecase import AbstractUseCase
from src.member.repository import MemberRDBRepository
from src.session.entity import SessionEntity
from src.social.enums import SocialInviteRequestStatus
from src.social.repository import SocialRDBRepository
from src.social.service import SocialService
from .exceptions import *


class SocialInviteApprovalUsecase(AbstractUseCase):
    """ 친구 요청 수락하기 """

    def __init__(self):
        self.social_repository = SocialRDBRepository()
        self.social_service = SocialService()

        self.member_repository = MemberRDBRepository()

    def execute(self, session: SessionEntity, social_id: int):
        social = self.social_repository.find_by_pk(pk=social_id)
        if social is None:
            raise NotFoundSocial()

        if social.status == SocialInviteRequestStatus.APPROVAL.value:
            raise AlreadySocialApproval()

        social.approval()
        self.social_repository.save(social)
