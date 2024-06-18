import requests

from .exception import KaKaoAccessTokenIssuedFail


class KaKaoOAuthenticateToken:
    """ KaKao Oauth, Access Token """

    endpoint = "https://kauth.kakao.com/oauth/token"

    @classmethod
    def get_access_token(cls, client_id: str, redirect_uri: str, authorization_code: str, client_secret: str) -> dict:
        resp = requests.post(
            cls.endpoint,
            params={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "code": authorization_code,
                "client_secret": client_secret
            }
        )
        if resp.status_code == 200:
            data = resp.json()
            return data

        raise KaKaoAccessTokenIssuedFail()
