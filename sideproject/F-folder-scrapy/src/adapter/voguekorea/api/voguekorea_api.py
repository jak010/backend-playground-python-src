from __future__ import annotations

import json
import uuid
from typing import List

from src.adapter.voguekorea.api.abstract import AbstractApiInterface
from src.adapter.voguekorea.api.libs.dto import FashionTrends, VogueKoreaDto
from src.adapter.voguekorea.pipe import (
    VugueKoreaScrapPipeLine,
    SelectElementTagFilter,
    ExtractContentTagFilter,
    ExcludeElementTagFilter,
    InitContentTagFilterAbstract
)


class VogueKoreaApi(AbstractApiInterface):
    HOST = "https://www.vogue.co.kr"

    def get_fashion_trends(self, page: int, item_per_page: int) -> FashionTrends:
        response = self.post(
            url=self.HOST + "/wp-admin/admin-ajax.php",
            data={
                "action": "get_posts_custom_v2",
                "posts_per_page": item_per_page,
                "post_type": "post",
                "paged": page,
                "tax1_slug": "fashion",
                "tax2_slug": "fashion-trend",
                "term2_id": 42
            })

        if response.status_code == 200:
            return FashionTrends.from_dict(json.loads(json.dumps(response.json())))

    def emit(self, page, item_per_page) -> List[VogueKoreaDto]:
        results = []

        trends = self.get_fashion_trends(page=page, item_per_page=item_per_page)
        for trend in trends.current_posts:
            resp = self.get(self.HOST + trend.permalink)

            pipeline = VugueKoreaScrapPipeLine(init_filter=InitContentTagFilterAbstract(html_source=resp.text))
            pipeline.append_filter(SelectElementTagFilter())
            pipeline.append_filter(ExcludeElementTagFilter())
            pipeline.append_filter(ExtractContentTagFilter())
            pipeline.start()

            results.append(VogueKoreaDto(
                id=None,
                trace_id=uuid.uuid4(),
                reference_id=int(trend.post_id),
                reference_date=trend.post_date,
                reference_link=self.HOST + trend.permalink,
                title=trend.post_title,
                content=pipeline.get_result(),
                thumbnail=trend.post_thumbnail_url
            ))
        return results
