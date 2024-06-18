from datetime import datetime
from typing import List

from src.adapter import slack
from src.adapter.kmodes.api.kmodes_api import KmodesApi
from src.adapter.kmodes.api.libs.dto import KmodesDto


class KmodesService:

    def __init__(self):
        self.api: KmodesApi = KmodesApi()

    def fetch_content_list(self, page: int) -> List[str]:
        return self.api.get_content_list(page=page)

    def fetch_content(self, url: str) -> KmodesDto:
        return self.api.get_fashion_content(url=url)

    @staticmethod
    def not_exist_reference_ids(
            fetched_reference_ids: List[int],
            saved_reference_ids: List[int]
    ) -> set[int]:
        return set(fetched_reference_ids) - set(saved_reference_ids)

    @staticmethod
    def to_datetime(reference_date: str):
        try:
            return datetime.strptime(reference_date, "%Y. %m. %d. %H:%M")
        except ValueError:
            return datetime.now()

    @staticmethod
    def is_stop_collect(reference_date: datetime) -> bool:
        if reference_date.year < 2023:
            return True
        return False

    @staticmethod
    def update_notify(count) -> True:
        if count == 0:
            slack.send_to_slack(data="[INFO] Kmodes Update Missing")
        if count != 0:
            slack.send_to_slack(data=f"[INFO] Kmodes Update ..{count}")

    @staticmethod
    def logging(logger, data):
        _log_message = f"{datetime.now()} [Kmodes] Fetch Data ...{data}"
        logger.info(_log_message)
