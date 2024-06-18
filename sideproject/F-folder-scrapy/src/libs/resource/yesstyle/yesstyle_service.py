import datetime
from typing import List

from src.adapter.yesstyle.api.libs.dto import YesstyleDto
from src.adapter.yesstyle.api.yesstyle_api import YesstyleAPI


class YesstyleService:

    def __init__(self):
        self.api: YesstyleAPI = YesstyleAPI()

    def fetch_content_list(self, page: int) -> List[str]:
        return self.api.get_fashion_content_links(page=page)

    def fetch_content(self, url) -> YesstyleDto:
        return self.api.get_fashion_content(url=url)

    def not_exist_content(self, fetched_contents_by_titles, saved_contents_by_titles):

        return set(fetched_contents_by_titles) - set(saved_contents_by_titles)

    def to_datetime(self, times):
        return datetime.datetime.fromisoformat(times)
