from __future__ import annotations

from typing import List, Optional

from src.adapter.fashionchingu.api.abstract import AbstractApiInterface
from src.adapter.fashionchingu.pipe import link_filters, entry_content_filters
from src.adapter.fashionchingu.pipe.pipes import FashionChinguLinkScrapPipeLine, FashionChinguScrapPipeLine

from src.adapter.fashionchingu.api.libs.dto import FashionChinguDto


class FashionChinguApi(AbstractApiInterface):
    HOST = "https://www.fashionchingu.com/blog"

    def get_links(self, page: int) -> Optional[List[str]]:
        resp = self.get(url=self.HOST + "/page/" + str(page))
        if resp:
            pipeline = FashionChinguLinkScrapPipeLine(init_filter=link_filters.InitContentTagFilter(
                html_source=resp.text
            ))
            pipeline.append_filter(link_filters.SelectElementTagFilter())
            pipeline.append_filter(link_filters.ExtractContentTagFilter())
            pipeline.start()

            return pipeline.get_result()

        return None

    def emit(self, link) -> FashionChinguDto:
        resp = self.get(url=link)
        if resp.status_code == 200:
            pipeline = FashionChinguScrapPipeLine(
                init_filter=entry_content_filters.InitContentTagFilterAbstractScrapFilter(
                    html_source=resp.text
                ))
            pipeline.append_filter(entry_content_filters.SelectElementTagFilter())
            pipeline.append_filter(entry_content_filters.ExtractContentTagFilter())
            pipeline.start()

            data = pipeline.get_result()
            return FashionChinguDto.new(
                reference_id=None,
                reference_date=data['reference_date'],
                reference_link=link,
                title=data['title'],
                content=data['content'],
                thumbnail=data['imgs'][0] if data['imgs'] else ""
            )
