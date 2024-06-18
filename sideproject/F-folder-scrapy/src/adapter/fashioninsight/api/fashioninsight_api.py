from __future__ import annotations

import uuid
from typing import List

import fake_useragent
import requests

from src.adapter.fashioninsight.api.libs.dto import FashionInsightDto
from src.adapter.fashioninsight.pipe import (
    content_list_filter,
    content_retrieve_filter
)
from src.adapter.fashioninsight.pipe import pipes


class FashionInsightApi:
    HOST = "https://www.fi.co.kr"
    UserAgent = fake_useragent.UserAgent().random

    def get_content_list(self, page: int) -> List[str]:
        _endpoint = "/main/list.asp"
        params = {
            "SectionStr": "News",
            "SectionSub": "",
            "page": page
        }
        r = requests.get(self.HOST + _endpoint,
                         params=params,
                         headers={"User-Agent": self.UserAgent})
        if r.status_code == 200:
            try:
                content = r.content.decode("euc-kr")
            except UnicodeDecodeError as e:
                content = r.text

            pipeline = pipes.FashionInsightScrapPipeLine(
                init_filter=content_list_filter.InitContentTagFilter(html_source=content))
            pipeline.append_filter(content_list_filter.SelecContentTagFilter())
            pipeline.append_filter(content_list_filter.ExtractContentTagFilter())
            pipeline.start()

            return pipeline.get_result()

    def get_content_retrieve(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            pipeline = pipes.FashionInsightScrapPipeLine(
                init_filter=content_retrieve_filter.InitContentTagFilter(html_source=r.text))
            pipeline.append_filter(content_retrieve_filter.ExtractContentTagFilter())
            pipeline.start()
            data = pipeline.get_dict()
            return {
                "reference_id": url.split("=")[-1],
                "reference_date": data["reference_date"],
                "reference_link": url,
                "title": data["title"],
                "content": data["content"],
                'thumbnail': data['thumbnail']
            }

    def emit(self, url) -> FashionInsightDto:
        data = self.get_content_retrieve(url=url)
        return FashionInsightDto.new(
            trace_id=uuid.uuid4(),
            reference_id=url.split("=")[-1],
            reference_date=data["reference_date"],
            reference_link=data['reference_link'],
            title=data["title"],
            content=data["content"],
            thumbnail=data['thumbnail']
        )

    def emit_by_id(self, idx: str) -> FashionInsightDto:
        data = self.get_content_retrieve(url='https://www.fi.co.kr/main/view.asp?idx=' + str(idx))
        return FashionInsightDto.new(
            trace_id=uuid.uuid4(),
            reference_id=idx,
            reference_date=data["reference_date"],
            reference_link=data['reference_link'],
            title=data["title"],
            content=data["content"],
            thumbnail=data['thumbnail']
        )
