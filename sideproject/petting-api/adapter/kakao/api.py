from __future__ import annotations

from adapter.kakao.libs.config import KaKaoConfig
from .resource.oauth.entry import KaKaoOauthResourceEntry
from .resource.oidc.entry import KaKaoOIDCResourceEntry
from .resource.token.entry import KaKaoAccessTokenResourceEntry
from .resource.user.entry import KaKaoUserResourceEntry
from .resource.geo.entry import KaKaoGeoResourceEntry


class KaKaoApi:

    def __init__(self, kakao_config: KaKaoConfig):
        self.config = kakao_config

    @property
    def oauth(self) -> KaKaoOauthResourceEntry:
        return KaKaoOauthResourceEntry(config=self.config)

    @property
    def user(self) -> KaKaoUserResourceEntry:
        return KaKaoUserResourceEntry(config=self.config)

    @property
    def oidc(self) -> KaKaoOIDCResourceEntry:
        return KaKaoOIDCResourceEntry(config=self.config)

    @property
    def token(self) -> KaKaoAccessTokenResourceEntry:
        return KaKaoAccessTokenResourceEntry(config=self.config)

    @property
    def local(self) -> KaKaoGeoResourceEntry:
        return KaKaoGeoResourceEntry(config=self.config)
