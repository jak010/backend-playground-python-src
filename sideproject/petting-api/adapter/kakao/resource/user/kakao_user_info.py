import json

import requests


class KaKaoUserInfo:
    """https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#req-user-info"""

    endpoint = "https://kapi.kakao.com/v2/user/me"

    @classmethod
    def get_user_info(cls,
                      access_token: str,
                      with_profile=False,
                      with_name=False,
                      with_email=False,
                      with_age_range=False,
                      with_birthday=False,
                      with_gender=False
                      ) -> dict:
        property_keys = []
        if with_profile:
            property_keys.append('kakao_account.profile')
        if with_name:
            property_keys.append('kakao_account.name')
        if with_email:
            property_keys.append('kakao_account.email')
        if with_age_range:
            property_keys.append('kakao_account.age_range')
        if with_birthday:
            property_keys.append('kakao_account.birtday')
        if with_gender:
            property_keys.append("kakao_account.gender")

        if property_keys:
            params = json.dumps(property_keys)

            resp = requests.get(
                cls.endpoint,
                params={"property_keys": params},
                headers={"Authorization": f"Bearer {access_token}"}
            )
        else:
            resp = requests.get(
                cls.endpoint, headers={
                    "Authorization": f"Bearer {access_token}"
                })

        if resp.status_code == 200:
            return resp.json()

        raise Exception(f"[KaKao User Failure]: {resp.content}")
