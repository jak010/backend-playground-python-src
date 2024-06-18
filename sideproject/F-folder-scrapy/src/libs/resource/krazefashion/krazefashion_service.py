from datetime import datetime
from typing import List

from src.adapter import slack
from src.adapter.krazefashion.api.krazefashion_api import KrazeFashionApi
from src.adapter.krazefashion.api.libs.dto import KrazeFashionDto


class KrazeFashionService:

    def __init__(self):
        self.api: KrazeFashionApi = KrazeFashionApi()

    def fetch_content_list(self) -> List[str]:
        return self.api.get_content_list()

    def fetch_content(self, url) -> KrazeFashionDto:
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
            slack.send_to_slack(data="[INFO] KrazeFashion Update Missing")
        if count != 0:
            slack.send_to_slack(data=f"[INFO] KrazeFashion Update ..{count}")

    @staticmethod
    def logging(logger, data):
        _log_message = f"{datetime.now()} [KrazeFashion] Fetch Data ...{data}"
        logger.info(_log_message)
