import datetime
import logging
from typing import List

from src.adapter.fashioninsight.api.fashioninsight_api import FashionInsightApi
from src.adapter.fashioninsight.api.libs.dto import FashionInsightDto

FASHIONINSIGHT_SERVICE_LOGGER = logging.getLogger("uvicorn.error")


class FashionInsightService:

    def __init__(self):
        self.api: FashionInsightApi = FashionInsightApi()

    def fetch_content_list(self, page: int) -> List[str]:
        return self.api.get_content_list(page=page)

    def fetch_content(self, url) -> FashionInsightDto:
        return self.api.emit(url=url)

    def fetch_content_by_idx(self, idx) -> FashionInsightDto:
        return self.api.emit_by_id(idx=idx)

    @staticmethod
    def is_stop_collect(reference_date: datetime.datetime):
        to_date = FashionInsightService.to_datetime(reference_date)
        if to_date.year == 2023 and to_date.month == 10:
            return True
        return False

    @staticmethod
    def to_datetime(reference_date):
        return datetime.datetime.strptime(reference_date, '%Y-%m-%d')

    @staticmethod
    def not_exist_reference_ids(fetch_contents: List[int], save_contents: List[int]):
        return set(fetch_contents) - set(save_contents)

    @staticmethod
    def update_notify(count: int):
        from src.adapter import slack
        if count == 0:
            slack.send_to_slack(data="[INFO]FashionInsight Update Missing")
        if count > 0:
            slack.send_to_slack(data=f"[INFO]FashionInsight Update ..{count}")

    @staticmethod
    def logging(data):
        _log_message = f"{datetime.datetime.now()} [FashionInsight] Fetch Data ...{data}"
        FASHIONINSIGHT_SERVICE_LOGGER.info(_log_message)
