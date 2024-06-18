from adapter.kakao.resource.abstract import AbstractKaKaoResource
from .dto.kakao_user_info_dto import KaKaoUserInfoDto

from .kakao_user_info import KaKaoUserInfo
from .kakao_user_logout import KaKaoUserLogOut


class KaKaoUserResourceEntry(AbstractKaKaoResource):

    def info(self,
             access_token: str,
             with_profile=False,
             with_name=False,
             with_email=False,
             with_age_range=False,
             with_birthday=False,
             with_gender=False
             ) -> KaKaoUserInfoDto:
        user_info = KaKaoUserInfo.get_user_info(
            access_token=access_token,
            with_profile=with_profile,
            with_name=with_name,
            with_email=with_email,
            with_age_range=with_age_range,
            with_birthday=with_birthday,
            with_gender=with_gender
        )
        return KaKaoUserInfoDto(**user_info)

    def logout(self, access_token):
        return KaKaoUserLogOut.user_logout(access_token=access_token)
