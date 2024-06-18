from __future__ import annotations

import datetime
import logging
from typing import List

from src.adapter import slack
from src.adapter.unnielooks.api.libs.dto import UnnieLooksDto
from src.adapter.unnielooks.api.unnielooks_api import UnnieLooksApi

UNNIELOOKS_SERVICE_LOGGER = logging.getLogger("uvicorn.error")


class UnnieLooksService:

    def __init__(self):
        self.api: UnnieLooksApi = UnnieLooksApi()

    def fetch_links(self, page: int) -> List[str]:
        return self.api.get_content_list(page=page)

    def fetch_content(self, url) -> UnnieLooksDto:
        return self.api.get_content(url=url)

    @staticmethod
    def not_exist_content_by_titles(fetched_contents_titles: List[str], saved_contents_titles: List[str]):
        return set(fetched_contents_titles) - set(saved_contents_titles)

    @staticmethod
    def to_datetime(reference_date: str):
        return datetime.datetime.strptime(reference_date, '%Y-%m-%d %H:%M:%S %z')

    @staticmethod
    def is_stop_collect(reference_date: datetime) -> bool:
        stop_year = 2022
        d = UnnieLooksService.to_datetime(reference_date)
        if d.year == stop_year and d.month == 5:
            return True
        return False

    @staticmethod
    def update_notify(count) -> True:
        if count == 0:
            slack.send_to_slack(data="[INFO] Unnielooks Update Missing")
        if count != 0:
            slack.send_to_slack(data=f"[INFO] Unnielooks Update ..{count}")

    @staticmethod
    def logging(data):
        _log_message = f"{datetime.datetime.now()} [Unnielooks] Fetch Data ...{data}"
        UNNIELOOKS_SERVICE_LOGGER.info(_log_message)
