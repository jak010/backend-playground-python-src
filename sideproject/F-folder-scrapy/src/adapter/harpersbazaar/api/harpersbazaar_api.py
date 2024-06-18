from __future__ import annotations

import uuid
from typing import List, Optional

import backoff
import fake_useragent
import requests

from src.adapter.harpersbazaar.api.libs.dto import HarpersBazaarDto
from src.adapter.harpersbazaar.pipe import content_list_filter, content_filter
from src.adapter.harpersbazaar.pipe.pipes import HarpersBazaarScrapPipeLine


class HarpersBazaarApi:
    HOST = "https://www.harpersbazaar.co.kr"
    UserAgent = fake_useragent.UserAgent().random

    @backoff.on_exception(backoff.expo, requests.exceptions.ReadTimeout, max_tries=5)
    def get_content_urls(self, page) -> Optional[List[str]]:
        _endpoint = "/fashion"

        resp = requests.post(
            url=self.HOST + _endpoint,
            headers={"User-Agent": self.UserAgent},
            data={
                "page": page,
                "page_type": "infiniti"
            },
            timeout=5
        )
        if resp.status_code == 200:
            pipeline = HarpersBazaarScrapPipeLine(
                init_filter=content_list_filter.InitContentTagFilter(html_source=resp.text)
            )
            pipeline.append_filter(content_list_filter.ExtractContentTagFilter())
            pipeline.start()
            return pipeline.get_data()

        return []

    def get_content(self, url) -> HarpersBazaarDto:
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            pipeline = HarpersBazaarScrapPipeLine(
                init_filter=content_filter.InitContentTagFilter(html_source=resp.text)
            )
            pipeline.append_filter(content_filter.SelectContentTagFilter())
            pipeline.append_filter(content_filter.ExtractContentTagFilter())
            pipeline.start()

            data = pipeline.get_data()
            return HarpersBazaarDto.new(
                trace_id=uuid.uuid4(),
                reference_id=url.split("/")[-1],
                reference_date=data['reference_date'],
                reference_link=url,
                title=data['title'],
                content=data['content'],
                thumbnail=data['imgs'][0] if data['imgs'] else url
            )
