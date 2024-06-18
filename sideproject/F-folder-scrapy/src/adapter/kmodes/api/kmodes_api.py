from __future__ import annotations

from typing import List, Optional
from urllib.parse import urlparse, parse_qs

import fake_useragent
import requests

from src.adapter.kmodes.api.libs.dto import KmodesDto
from src.adapter.kmodes.pipe import content_filter, content_list_filter
from src.adapter.kmodes.pipe import pipes


class KmodesApi:
    HOST = "https://blog.naver.com"
    UserAgent = fake_useragent.UserAgent().random

    def get_content_list(self, page: int) -> Optional[List[str]]:
        _endpoint = "/PostList.naver"
        params = {
            "from": "postList",
            "blogId": "kmodes",
            "categoryNo": 1,
            "parentCategoryNo": 1,
            "currentPage": page
        }
        r = requests.get(self.HOST + _endpoint,
                         params=params,
                         headers={"User-Agent": self.UserAgent})
        if r.status_code == 200:
            pipeline = pipes.KmodesScrapPipeLine(
                init_filter=content_list_filter.InitContentTagFilter(html_source=r.text))

            pipeline.append_filter(content_list_filter.SelecContentTagFilter())
            pipeline.append_filter(content_list_filter.ExtractContentTagFilter())
            pipeline.start()

            return pipeline.get_result()
        else:
            return []

    def get_fashion_content(self, url: str) -> KmodesDto:
        r = requests.get(url, headers={"User-Agent": self.UserAgent})

        if r.status_code == 200:
            pipeline = pipes.KmodesScrapPipeLine(init_filter=content_filter.InitContentTagFilter(
                html_source=r.text))
            pipeline.append_filter(content_filter.ExtractContentTagFilter())
            pipeline.start()

            data = pipeline.get_data()
            return KmodesDto.new(
                reference_id=self._parse_querystring(url)['logNo'],
                reference_date=data['reference_date'],
                reference_link=url,
                title=data['title'],
                content=data['content'],
                thumbnail=data['thumbnail']
            )

    def _parse_querystring(self, url: str) -> Optional[dict]:
        urlparsed = urlparse(url)
        querystring = parse_qs(urlparsed.query)
        return {
            "blogId": querystring.get('blogId', None)[0],
            "logNo": querystring.get('logNo', None)[0],
            "categoryNo": querystring.get('categoryNo', None)[0],
            "parentCategoryNo": querystring.get('parentCategoryNo', None)[0],
            "from": querystring.get('from', None)[0]
        }
