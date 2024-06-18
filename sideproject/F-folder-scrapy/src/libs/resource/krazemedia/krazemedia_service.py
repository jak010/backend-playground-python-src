from datetime import datetime
from typing import List

from src.adapter import slack
from src.adapter.krazemedia.api.krazemedia_api import KrazeMediaApi
from src.adapter.krazemedia.api.libs.dto import KrazeMediaDto


class KrazeMediaService:

    def __init__(self):
        self.api: KrazeMediaApi = KrazeMediaApi()

    def fetch_kdrama_content_list(self) -> List[str]:
        return self.api.get_kdramas_content_list()

    def fetch_tvmovies_content_list(self) -> List[str]:
        return self.api.get_tvmovies_content_list()

    def fetch_content(self, url) -> KrazeMediaDto:
        return self.api.get_content(_endpoint=url)

    @staticmethod
    def not_exist_titles(fetched_titles: List[str], saved_titles: List[str]) -> set[str]:
        return set(fetched_titles) - set(saved_titles)

    @staticmethod
    def to_datetime(reference_date: str):
        return datetime.strptime(reference_date, '%Y-%m-%d')

    @staticmethod
    def update_notify(count) -> True:
        if count == 0:
            slack.send_to_slack(data="[INFO] KrazeMedia Update Missing")
        if count != 0:
            slack.send_to_slack(data=f"[INFO] KrazeMedia Update ..{count}")

    @staticmethod
    def logging(logger, data):
        _log_message = f"{datetime.now()} [KrazeMedia] Fetch Data ...{data}"
        logger.info(_log_message)
