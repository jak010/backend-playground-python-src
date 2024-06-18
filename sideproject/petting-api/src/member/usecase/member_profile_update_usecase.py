from dependency_injector.wiring import Provide

from adapter.kakao.api import KaKaoApi
from libs.abstract.abstract_usecase import AbstractUseCase
from settings.container.adapter_container import (
    KaKaoAdapterContainer as _KaKaoAdapterContainer
)
from src.authenticate.usecase import KaKaoAuthenticateFailureException
from src.member.controller.request import MemberProfileUpdateFormDTO
from src.member.repository import (
    MemberRDBRepository,
    MemberProfileRDBRepository
)
from src.member.service import MemberService
from src.session.entity import SessionEntity


class InvalidRequestAddress(Exception):
    """ 입력된 주소를 찾을 수 없음  """


class MemberProfileUpdateUseCase(AbstractUseCase):
    kakao_api: KaKaoApi = Provide[_KaKaoAdapterContainer.kako_api]

    def __init__(self):
        self.member_service = MemberService()

        self.member_rdb_repository = MemberRDBRepository()
        self.member_profile_rdb_repository = MemberProfileRDBRepository()

    def execute(self,
                session: SessionEntity,
                request: MemberProfileUpdateFormDTO
                ):
        try:
            kakao_local_search = self.kakao_api.local.get_local_search(address=request.address)
        except Exception as e:
            raise KaKaoAuthenticateFailureException from e

        if not bool(kakao_local_search.meta.total_count):
            raise InvalidRequestAddress()

        self.member_profile_rdb_repository.update_profile(
            member_id=session.member_id,
            nickname=request.nickname,
            description=request.description,
            address=kakao_local_search.documents[0].address_name,
            region1=kakao_local_search.documents[0].road_address.region_1depth_name,
            region2=kakao_local_search.documents[0].road_address.region_2depth_name,
            region3=kakao_local_search.documents[0].road_address.region_3depth_name,
            road_name=kakao_local_search.documents[0].road_address.road_name,
            latitude=round(float(kakao_local_search.documents[0].y), 5),
            longitude=round(float(kakao_local_search.documents[0].x), 5),
            job=request.job,
            birthday=request.birthday,
            gender=request.gender,
            mbti=request.mbti
        )
