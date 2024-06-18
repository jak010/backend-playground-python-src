import datetime
import logging
from typing import List, NewType

from src.adapter import slack
from src.adapter.eyesmag.api.eyesmag_api import EyesMagApi
from src.adapter.eyesmag.api.libs.dto import EyesMagDto

EYESMAG_USECASE_LOGGER = logging.getLogger("uvicorn.error")

END_FETCH_LIMIT_YEAR = 2021

EYESMAG_TITLE = NewType('EYESMAG_TITLE', str)


class EyesMagService:

    def __init__(self):
        self.api: EyesMagApi = EyesMagApi()

    def fetched_data(self, page: int) -> List[EyesMagDto]:
        return self.api.emit(page=page)

    @staticmethod
    def not_exist_content_by_title(fetched_contents_by_titles: list, saved_contents_by_titles: list):
        return set(fetched_contents_by_titles) - set(saved_contents_by_titles)

    @staticmethod
    def to_datetime(reference_date):
        return datetime.datetime.strptime(reference_date, '%Y-%m-%dT%H:%M:%S.%fZ')

    @staticmethod
    def update_notify(count):
        if count == 0:
            slack.send_to_slack(data="[INFO]EyesMag Update Missing")
        if count != 0:
            slack.send_to_slack(data=f"[INFO]EyesMag Update ..{count}")

    @staticmethod
    def logging(logger, data):
        _log_message = f"{datetime.datetime.now()} [INFO] Fetch Data ...{data}"
        logger.info(_log_message)

    def is_stop_collect(self, reference_date):
        if self.to_datetime(reference_date).year == 2021:
            return True
        return False
