from adapter.kakao.resource.abstract import AbstractKaKaoResource

from .kakao_oidc_user_info import KaKaoOIDCUserInfo


class KaKaoOIDCResourceEntry(AbstractKaKaoResource):

    def user_info(self, access_token: str):
        return KaKaoOIDCUserInfo.get_user_info(access_token=access_token)
