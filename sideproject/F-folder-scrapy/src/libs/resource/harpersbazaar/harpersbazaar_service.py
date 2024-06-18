import datetime
from typing import List

from src.adapter.harpersbazaar.api.harpersbazaar_api import HarpersBazaarApi
from src.adapter.harpersbazaar.api.libs.dto import HarpersBazaarDto


class HarpersBazaarService:

    def __init__(self):
        self.api: HarpersBazaarApi = HarpersBazaarApi()

    def fetch_links(self, page: int) -> List[str]:
        return self.api.get_content_urls(page=page)

    def fetch_content(self, url) -> HarpersBazaarDto:
        return self.api.get_content(url=url)

    def not_exist_content_by_id(self,
                                fetched_contents_reference_ids: list[int],
                                saved_contents_reference_ids: list[int]):
        return set(fetched_contents_reference_ids) - set(saved_contents_reference_ids)

    def to_datetime(self, reference_date: str) -> datetime.datetime:
        return datetime.datetime.strptime(reference_date, '%Y.%m.%d')

    def is_stop_collect(self, reference_date: datetime.datetime) -> bool:
        if reference_date.year == 2022 and reference_date.month == 12:  # 수집대상 데이터는 23년한정
            return True
        return False
