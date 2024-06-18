from __future__ import annotations

import uuid

import backoff
import fake_useragent
import requests

from src.adapter.unnielooks.api.libs.dto import UnnieLooksDto
from src.adapter.unnielooks.pipe import link_filters, content_filters
from src.adapter.unnielooks.pipe.pipes import UnnieLooksLinkScrapPipeLine, UnnieLooksScrapPipeLine
from src.adapter.utils import ByPassRequestMixin


class UnnieLooksApi(ByPassRequestMixin):
    HOST = "https://unnielooks.com"
    UserAgent = fake_useragent.UserAgent().random

    @backoff.on_exception(backoff.expo, requests.exceptions.ReadTimeout, max_tries=5)
    def get_content_list(self, page: int):
        _endpoint = "/en-kr/blogs/news"
        params = {"page": page}

        resp = self.request.get(
            url=self.HOST + _endpoint,
            headers={"User-Agent": self.UserAgent},
            params=params
        )
        if resp.status_code == 200:
            pipline = UnnieLooksLinkScrapPipeLine(init_filter=link_filters.InitContentTagFilter(html_source=resp.text))
            pipline.append_filter(link_filters.ExtractContentLinkFilter())
            pipline.start()
            return pipline.get_result()
        raise Exception(f"{self.__class__.__name__}:get_links, request failed")

    def get_content(self, url: str) -> UnnieLooksDto:
        resp = self.request.get(url=url, timeout=3)
        if resp.status_code == 200:
            pipeline = UnnieLooksScrapPipeLine(
                init_filter=content_filters.InitContentTagFilterAbstractScrapFilter(html_source=resp.text)
            )
            pipeline.append_filter(content_filters.ExtractContentTagFilter())
            pipeline.start()

            data = pipeline.get_result()

            return UnnieLooksDto.new(
                trace_id=uuid.uuid4(),
                reference_id=data['reference_id'],
                reference_date=data['reference_date'],
                reference_link=url,
                title=data['title'],
                content='\n'.join([x for x in data["content"] if x]),
                thumbnail=data['thumbnail']
            )
