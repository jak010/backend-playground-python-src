from __future__ import annotations

from adapter.kakao.resource.abstract import AbstractKaKaoResource
from .dto.kakao_access_token_dto import KaKaoAccessTokenDto
from .kakao_oauth_authorize_url import KaKaoOAuthorizeUrl
from .kakao_oauthenticate_token import KaKaoOAuthenticateToken


class KaKaoOauthResourceEntry(AbstractKaKaoResource):

    def get_authorization_url(self) -> str:
        return KaKaoOAuthorizeUrl.get_authorized_url(
            client_id=self.config.client_id,
            redirect_uri=self.config.redirect_uri
        )

    def get_access_token(self, authorization_code: str) -> KaKaoAccessTokenDto:
        kakao_access_token = KaKaoOAuthenticateToken.get_access_token(
            client_id=self.config.client_id,
            redirect_uri=self.config.redirect_uri,
            authorization_code=authorization_code,
            client_secret=self.config.client_secret
        )
        return KaKaoAccessTokenDto(**kakao_access_token)
