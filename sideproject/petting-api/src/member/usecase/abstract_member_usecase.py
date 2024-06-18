from __future__ import annotations

from dependency_injector.wiring import Provide

from adapter.kakao.api import KaKaoApi
from libs.abstract.abstract_usecase import AbstractUseCase
from settings.container.adapter_container import (
    KaKaoAdapterContainer as _KaKaoAdapterContainer
)
from src.member.repository import (
    MemberRDBRepository,
    MemberProfileRDBRepository
)
from src.pet.repository import (
    PetRDBRepository,
    PetAttachmentRDBRepository
)
from src.member.service import MemberService


class AbstractMemberUseCase(AbstractUseCase):
    kakao_api: KaKaoApi = Provide[_KaKaoAdapterContainer.kako_api]

    def __init__(self):
        self.member_service = MemberService()

        self.member_rdb_repository = MemberRDBRepository()
        self.member_profile_rdb_repository = MemberProfileRDBRepository()
        self.pet_rdb_repository = PetRDBRepository()
        self.pet_attachment_rdb_repository = PetAttachmentRDBRepository()
