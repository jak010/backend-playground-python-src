from __future__ import annotations

from typing import List, Optional

import fake_useragent

from src.adapter.utils import ByPassRequestMixin
from src.adapter.yesstyle.api.libs.dto import YesstyleDto
from src.adapter.yesstyle.pipe import content_links_filter, content_filter
from src.adapter.yesstyle.pipe.pipes import YesstyleScrapPipeLine


class YesstyleAPI(ByPassRequestMixin):
    HOST = "https://www.yesstyle.com"
    UserAgnet = fake_useragent.UserAgent().random

    def get_fashion_content_links(self, page: int) -> Optional[List[str]]:
        _endpoint = f"/blog/category/fashion/page/{page}"

        resp = self.request.get(url=self.HOST + _endpoint, timeout=5)
        if resp.status_code == 200:
            pipe = YesstyleScrapPipeLine(init_filter=content_links_filter.InitContentTagFilterAbstract(
                html_source=resp.text
            ))
            pipe.append_filter(content_links_filter.SelectElementTagFilter())
            pipe.append_filter(content_links_filter.ExtractContentTagFilter())
            pipe.start()
            resp.close()
            return pipe.get_data()
        return []

    def get_fashion_content(self, url: str) -> YesstyleDto:
        resp = self.request.get(url=url)
        if resp.status_code == 200:
            pipe = YesstyleScrapPipeLine(init_filter=content_filter.InitContentTagFilter(
                html_source=resp.text
            ))
            pipe.append_filter(content_filter.SelectElementTagFilter())
            pipe.append_filter(content_filter.ExtractContentTagFilter())
            pipe.start()

            data = pipe.get_data()
            resp.close()
            return YesstyleDto.new(
                title=data['title'],
                content=data['content'],
                thumbnail=data['thumbnail'],
                reference_link=url,
                reference_id=None,
                reference_date=data['reference_date']
            )
