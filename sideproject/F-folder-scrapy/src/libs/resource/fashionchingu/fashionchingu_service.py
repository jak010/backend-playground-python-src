import datetime
from typing import List

from src.adapter import slack
from src.adapter.fashionchingu.api.fashionchingu_api import FashionChinguApi
from src.adapter.fashionchingu.api.libs.dto import FashionChinguDto


class FashionChinguService:

    def __init__(self):
        self.api: FashionChinguApi = FashionChinguApi()

    def fetch_links(self, page: int) -> List[str]:
        return self.api.get_links(page=page)

    def fetch_content(self, link) -> FashionChinguDto:
        return self.api.emit(link=link)

    def not_exist_contents(self, fetched_content_titles, save_content_titles):
        return set(fetched_content_titles) - set(save_content_titles)

    @staticmethod
    def to_datetime(reference_date: str):
        return datetime.datetime.strptime(reference_date, '%d/%m/%Y')

    @staticmethod
    def logging(logger, data):
        _log_message = f"{datetime.datetime.now()} [FashionChingu] Fetch Data ...{data}"
        logger.info(_log_message)

    @staticmethod
    def update_notify(count) -> True:
        if count == 0:
            slack.send_to_slack(data="[INFO] FashionChingu Update Missing")
        if count != 0:
            slack.send_to_slack(data=f"[INFO] FashionChingu Update ..{count}")
