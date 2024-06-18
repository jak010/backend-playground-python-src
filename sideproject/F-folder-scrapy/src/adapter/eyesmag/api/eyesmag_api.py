from __future__ import annotations

from typing import List

from src.adapter.eyesmag.api.abstract import AbstractApiInterface
from src.adapter.eyesmag.api.libs.dto import EyesMagDto, Post
from src.adapter.eyesmag.pipe import (
    eyesmag_pipe,
    content_filter
)


class EyesMagApi(AbstractApiInterface):
    HOST = "https://www.eyesmag.com"

    def emit(self, page: int) -> List[EyesMagDto]:
        content_list: List[Post] = self.get_content_list(page=page)
        results = []
        for content in content_list:
            resp = self.get_content(id=content.ID, name=content.name)
            pipe = eyesmag_pipe.EyesMagScrapPipeLine(
                init_filter=content_filter.InitContentTagFilterAbstract(html_source=resp.text)
            )
            pipe.append_filter(content_filter.SelectContentFilter())
            pipe.append_filter(content_filter.ExcludeContentFilter())
            pipe.append_filter(content_filter.ExtractContentTagFilter())
            pipe.start()

            data = pipe.get_data()

            results.append(EyesMagDto(
                reference_id=content.ID,
                reference_date=content.publishedAt,
                reference_link=self.HOST + f"/posts/{content.ID}/{content.name}",
                title=content.title,
                content=data['content'],
                thumbnail="https://cdn.eyesmag.com/" + content.thumbnail
            ))

        return results

    def get_content_list(self, page: int) -> List[Post]:
        _endpoint = "/api/v1/posts"
        params = {
            "page": page,
            "taxonomy_id": 445
        }
        resp = self.get(url=self.HOST + _endpoint, params=params)
        if resp.status_code == 200:
            result = []
            for item in resp.json():
                item.pop('termRelationships.term_taxonomy_id')
                result.append(Post(**item))
            return result

    def get_content(self, id: int, name: str):
        _endpoint = f"/posts/{id}/{name}"
        return self.get(url=self.HOST + _endpoint)
