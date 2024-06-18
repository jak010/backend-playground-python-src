from __future__ import annotations

from adapter.kakao.resource.abstract import AbstractKaKaoResource
from .dto.kakao_access_token_info_dto import KaKaoAccessTokenInfoDto
from .kakao_access_token_info import KaKaoAccessTokenInfo


class KaKaoAccessTokenResourceEntry(AbstractKaKaoResource):

    def get_access_token_info(self, access_token: str) -> KaKaoAccessTokenInfoDto:
        return KaKaoAccessTokenInfo.get_access_token_info(access_token=access_token)
