from libs.abstract.abstract_usecase import AbstractUseCase

from src.session.entity import SessionEntity
from src.social.controller.request import SocialInviteRequestDto

from src.member.repository import MemberRDBRepository
from src.social.repository import SocialRDBRepository
from src.social.service import SocialService
from src.social.entity import SocialEntity

from .exceptions import *


class SocialInviteRequestUsecase(AbstractUseCase):
    """ 친구 요청 보내기 """

    def __init__(self):
        self.social_repository = SocialRDBRepository()
        self.social_service = SocialService()

        self.member_repository = MemberRDBRepository()

    def execute(self, session: SessionEntity = None, request: SocialInviteRequestDto = None):
        sender = session.member_id
        receiver = request.receiver_member

        member = self.member_repository.find_member_by_nanoid(nanoid=receiver)
        if member is None:
            raise NotFoundReceiverMember()

        social = self.social_repository.find_social_by_invited(sender=sender, receiver=receiver)
        if social is None:
            new_social = self.social_service.invite(sender=sender, receiver=receiver)
            self.social_repository.save(new_social)
            return social
        raise AlreadyRequestInvited()
