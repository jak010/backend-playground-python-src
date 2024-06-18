import requests
from adapter.aligo.resource.sms.dto import SMSSendResponseDto


class SMSApi:

    def __init__(self, mode: str, aligo_api_key: str, aligo_user_id: str, aligo_sender: str):
        self.is_test_mode = 'Y' if mode == "LOCAL" or mode == "DEV" else 'N'
        self.aligo_api_key = aligo_api_key
        self.aligo_user_id = aligo_user_id
        self.aligo_sender = aligo_sender  # phone

    def sms_send(self, receiver: str, title: str, message: str) -> SMSSendResponseDto:
        """ https://smartsms.aligo.in/admin/api/spec.html """
        _endpoint = 'https://apis.aligo.in/send/'
        resp = requests.post(url=_endpoint, data={
            'key': self.aligo_api_key,
            'userid': self.aligo_user_id,
            'sender': self.aligo_sender,
            'receiver': receiver,
            'msg': message,
            'msg_type': 'SMS',
            'title': title,
            'testmode_yn': self.is_test_mode
        })
        if resp.status_code == 200:
            response_data = resp.json()
            if response_data['result_code'] == -201:
                raise Exception("Aligo Not Enough Resource")  # TODO 24.04.04 보유건수 부족 알림이 발생, 모니터링 할 수 있도록 조치 필요함
            else:
                return SMSSendResponseDto(**response_data)

    def get_sms_detail(self, mid: int):
        _endpoint = 'https://apis.aligo.in/sms_list/'
        resp = requests.post(url=_endpoint, data={
            'key': self.aligo_api_key,
            'userid': self.aligo_user_id,
            'mid': mid,
            'page': '1',  # 페이지 번호
            'page_size': '30'  # 페이지당 출력갯수 (30~500)
        })
        if resp.status_code == 200:
            return resp.json()
