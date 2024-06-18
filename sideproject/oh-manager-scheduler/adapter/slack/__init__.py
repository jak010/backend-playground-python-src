from slack_sdk.web.client import WebClient
from functools import cached_property


class Notification:

    def __init__(self, token, channel):
        self.token = token
        self.channel = channel

    @cached_property
    def client(self) -> WebClient:
        return WebClient(token=self.token)

    def send_message(self, data: str):
        self.client.chat_meMessage(channel=self.channel, text=data)
