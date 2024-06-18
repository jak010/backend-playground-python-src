import os

from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()

CHANNEL_ADMIN_NOTIFY = 'C062SDEDSAC'
CHANNEL_ADMIN_MONITORING = 'C063B6PR200'


def get_client():
    return WebClient(token=os.environ['SLACK_BOT_TOKEN'])


def send_to_slack(data: str):
    get_client().chat_postMessage(channel=CHANNEL_ADMIN_NOTIFY, text=data)


def send_to_error(data: str):
    get_client().chat_postMessage(channel=CHANNEL_ADMIN_MONITORING, text=data)
