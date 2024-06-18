import uuid

import requests


class KaKaoOAuthorizeUrl:
    """ KaKao Oauth, Authroization Code """
    endpoint = "https://kauth.kakao.com/oauth/authorize"

    @classmethod
    def get_authorized_url(cls, client_id: str, redirect_uri: str) -> str:
        resp = requests.get(
            cls.endpoint,
            params={
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "nonce": str(uuid.uuid4())
            })
        return resp.url
