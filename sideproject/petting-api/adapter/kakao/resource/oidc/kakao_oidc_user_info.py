import requests


class KaKaoOIDCUserInfo:
    endpoint = "https://kapi.kakao.com/v1/oidc/userinfo"

    @classmethod
    def get_user_info(cls, access_token: str):
        resp = requests.get(
            cls.endpoint,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        if resp.status_code == 200:
            return resp.json()
