from __future__ import annotations

import datetime
from typing import List

from src.adapter import slack
from src.adapter.voguekorea.api.libs.dto import VogueKoreaDto
from src.adapter.voguekorea.api.voguekorea_api import VogueKoreaApi


class VogueKoreaService:

    def __init__(self):
        self.vogue_korea_api = VogueKoreaApi()

    def fetch_contents(self, page, item_per_page) -> List[VogueKoreaDto]:
        return self.vogue_korea_api.emit(page=page, item_per_page=item_per_page)

    def get_post_ids(self, fetch_contents: List[VogueKoreaDto]) -> List[int]:
        return [int(each.reference_id) for each in fetch_contents]

    @staticmethod
    def not_exist_refernce_ids(
            fetched_conetents_ids: List[int],
            save_contents_ids: List[int]
    ) -> List[int]:
        return list(set(fetched_conetents_ids) - set(save_contents_ids))

    @staticmethod
    def to_datetime(reference_date: str):
        return datetime.datetime.strptime(reference_date, "%Y.%m.%d")

    @staticmethod
    def update_notify(count) -> True:
        if count == 0:
            slack.send_to_slack(data="[INFO] VogueKorea Update Missing")
        if count != 0:
            slack.send_to_slack(data=f"[INFO] VogueKorea Update ..{count}")

    @staticmethod
    def logging(logger, data):
        _log_message = f"{datetime.datetime.now()} [VogueKorea] Fetch Data ...{data}"
        logger.info(_log_message)
