from __future__ import annotations

import time
from typing import NoReturn, List

from src.config.context import Transactional
from src.libs.resource.abstracts.abstract_usecase import (
    AbstractUsecase,
    AbstractUsecaseCRUDImplements,
    AbstrctUsecaseCrawlerImplements

)
from src.libs.resource.common.define import CONVERT
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.fashioninsight.fashioninsight_entity import FashionInsightEntity
from src.libs.resource.fashioninsight.fashioninsight_service import FashionInsightService
from src.libs.resource.post.post_entity import PostEntity
from src.libs.utils.content_creator import ContentCreator


class FashionInsightUsecase(AbstractUsecase, AbstractUsecaseCRUDImplements, AbstrctUsecaseCrawlerImplements):
    service = FashionInsightService()

    def __init__(self):
        self._START_PAGE = 1

    @Transactional()
    def get_content_list(
            self,
            sort_key: str = None,
            sort_type: str = None,
            page: int = None,
            item_per_page: int = None
    ):
        return self.fashioninsight_repository.find_by(
            sort_key=sort_key,
            sort_type=sort_type,
            page=page,
            item_per_page=item_per_page
        )

    @Transactional()
    def get_content(self, trace_id: str) -> UniversalEntity:
        return self.fashioninsight_repository.find_by_trace_id(trace_id=trace_id)

    @Transactional()
    def get_count(self):
        return self.fashioninsight_repository.get_count()

    @Transactional()
    def convert(self, trace_id: str) -> NoReturn:
        fashioninsight = self.fashioninsight_repository.find_by_trace_id(trace_id=trace_id)

        if fashioninsight:
            post = self.post_repository.find_by_trace_id(trace_id=fashioninsight.trace_id)
            if post is None:
                llm_content = ContentCreator().summary(
                    fashioninsight.content + "\n\n" + fashioninsight.thumbnail
                )

                self.post_repository.add(PostEntity.new(
                    trace_id=fashioninsight.trace_id,
                    title=fashioninsight.title,
                    content=llm_content,
                    keyword="fashioninsight",
                    platform="fashioninsight",
                    thumbnail=fashioninsight.thumbnail,
                    reference_link=fashioninsight.reference_link,
                    created_at=int(time.time()),
                ))

                self.fashioninsight_repository.update_on_convert(
                    trace_id=fashioninsight.trace_id,
                    is_convert=CONVERT.ON
                )

                return {
                    "before_content": fashioninsight.content,
                    "after_content": llm_content
                }

    @Transactional()
    def daily_collect(self):
        """ 스케쥴링 처리를 위해 사용  """

        fetched_contents: list[str] = self.service.fetch_content_list(page=1)  # from, adapter
        fetched_contents_by_reference_ids = [int(content.split("=")[-1]) for content in fetched_contents]

        saved_contents = self.fashioninsight_repository.find_by_reference_ids(
            reference_ids=fetched_contents_by_reference_ids)
        saved_contents_by_reference_ids = [int(saved_content.reference_id) for saved_content in saved_contents]

        not_exist_ids = self.service.not_exist_reference_ids(
            fetch_contents=fetched_contents_by_reference_ids,
            save_contents=saved_contents_by_reference_ids
        )

        for not_exit_id in not_exist_ids:
            fashioninsight_dto = self.service.fetch_content_by_idx(idx=not_exit_id)
            self.fashioninsight_repository.add(
                fashioninsight_entity=FashionInsightEntity.from_dto(fashioninsight_dto)
            )

        self.service.update_notify(count=len(not_exist_ids))

    def all_collect(self):
        """ DB에 데이터를 fetch하기 위해 사용 """
        start_page = 1

        from src.adapter.fashioninsight.api.libs.dto import FashionInsightDto
        fashioninsight_dtos: List[FashionInsightDto] = []
        is_stop = False

        while True:
            if is_stop: break

            content_list = self.service.fetch_content_list(page=start_page)
            for content in content_list:
                fashioninsight_dto = self.service.fetch_content(url=content)

                self.service.logging(data=fashioninsight_dto.reference_date)

                if self.service.is_stop_collect(fashioninsight_dto.reference_date):
                    is_stop = True
                    break

                fashioninsight_dtos.append(fashioninsight_dto)

            start_page += 1

        with self.session.begin():
            for fashioninsight_dto in fashioninsight_dtos:
                fashioninsight_entity = self.fashioninsight_repository.find_by_reference_id(
                    int(fashioninsight_dto.reference_id)
                )
                if not fashioninsight_entity:
                    self.fashioninsight_repository.add(
                        fashioninsight_entity=FashionInsightEntity.from_dto(
                            fashioninsight_dto
                        ))

            self.service.update_notify(count=len(fashioninsight_dtos))
