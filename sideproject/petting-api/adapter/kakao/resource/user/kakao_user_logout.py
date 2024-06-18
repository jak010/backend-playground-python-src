import datetime

import requests

from libs.utils import logger


class KaKaoUserLogOut:
    """https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#logout"""

    endpoint = "https://kapi.kakao.com/v1/user/logout"

    @classmethod
    def user_logout(cls, access_token: str):
        resp = requests.get(
            cls.endpoint,
            headers={
                "Authorization": f"Bearer ${access_token}"
            }
        )
        if resp.status_code == 200:
            data = resp.json()
            logger.UVICORN_LOGGER.info(f'[{datetime.datetime.now()}][KAKAO][LOGOUT]:{data}')
            return data
