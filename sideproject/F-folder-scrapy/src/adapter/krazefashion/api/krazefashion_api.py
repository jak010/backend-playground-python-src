from __future__ import annotations

from typing import List, Optional

import fake_useragent
import requests

from src.adapter.krazefashion.api.libs.dto import KrazeFashionDto
from src.adapter.krazefashion.pipe import content_filter, content_list_filter
from src.adapter.krazefashion.pipe.pipes import KrazeFashionScrapPipeLine


class KrazeFashionApi:
    HOST = "https://thekrazemag.com"
    UserAgent = fake_useragent.UserAgent().random

    def get_content_list(self) -> Optional[List[str]]:
        _endpoint = "/fashion-beauty"

        r = requests.get(self.HOST + _endpoint, headers={"User-Agent": self.UserAgent})
        if r.status_code == 200:
            pipe = KrazeFashionScrapPipeLine(
                init_filter=content_list_filter.InitContentTagFilter(html_source=r.text))
            pipe.append_filter(content_list_filter.ExtractContentTagFilter())

            pipe.start()
            return pipe.get_data()
        return []

    def get_content(self, _endpoint: str) -> KrazeFashionDto:
        url = self.HOST + _endpoint
        r = requests.get(url, headers={"User-Agent": self.UserAgent})

        if r.status_code == 200:
            pipe = KrazeFashionScrapPipeLine(
                init_filter=content_filter.InitContentTagFilter(html_source=r.text))
            pipe.append_filter(content_filter.ExtractContentTagFilter())
            pipe.start()

            data = pipe.get_data()
            return KrazeFashionDto.new(
                reference_id=None,
                reference_date=data['reference_date'],
                reference_link=url,
                title=data['title'],
                content=data['content'],
                thumbnail=data['thumbnail']
            )
