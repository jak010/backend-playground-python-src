import requests


class KaKaoLocalSearchAddress:
    endpoint = "https://dapi.kakao.com/v2/local/search/address.json"

    @classmethod
    def get_user_info(cls, client_id: str, address: str):
        resp = requests.get(
            cls.endpoint,
            headers={
                "Authorization": f"KakaoAK {client_id}"
            },
            params={
                "query": address
            }
        )
        if resp.status_code == 200:
            return resp.json()
