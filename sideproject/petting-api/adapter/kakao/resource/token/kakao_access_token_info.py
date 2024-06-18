import requests

from .dto.kakao_access_token_info_dto import KaKaoAccessTokenInfoDto


class KaKaoAccessTokenInfo:
    """ https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#get-token-info """

    _endpoint = "https://kapi.kakao.com/v1/user/access_token_info"

    @classmethod
    def get_access_token_info(cls, access_token: str) -> KaKaoAccessTokenInfoDto:
        resp = requests.get(
            url=cls._endpoint,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        if resp.status_code == 200:
            data = resp.json()
            return KaKaoAccessTokenInfoDto(**data)
        raise Exception("KaKao Access Token Info Failure")
