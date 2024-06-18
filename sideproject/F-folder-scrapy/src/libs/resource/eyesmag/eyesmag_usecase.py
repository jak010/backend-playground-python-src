from __future__ import annotations

import logging
import time
from typing import List

from src.adapter.eyesmag.api.libs.dto import EyesMagDto
from src.config.context import Transactional
from src.libs.resource.abstracts.abstract_usecase import (
    AbstractUsecase,
    AbstractUsecaseCRUDImplements,
    AbstrctUsecaseCrawlerImplements
)
from src.libs.resource.common.define import CONVERT
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.eyesmag.eyesmag_entity import EyesMagEntity
from src.libs.resource.eyesmag.eyesmag_service import EyesMagService
from src.libs.resource.post.post_entity import PostEntity
from src.libs.utils.content_creator import ContentCreator

EYESMAG_USECASE_LOGGER = logging.getLogger("uvicorn.error")


class EyesMagUsecase(
    AbstractUsecase,
    AbstractUsecaseCRUDImplements[EyesMagEntity],
    AbstrctUsecaseCrawlerImplements
):

    def __init__(self):
        self.service = EyesMagService()

    @Transactional()
    def get_content_list(
            self,
            *,
            sort_key: str = None,
            sort_type: str = None,
            page: int = None,
            item_per_page: int = None
    ):
        return self.eyesmag_repository.find_by(
            sort_key=sort_key,
            sort_type=sort_type,
            page=page,
            item_per_page=item_per_page
        )

    @Transactional()
    def get_content(self, trace_id: str) -> UniversalEntity:
        return self.eyesmag_repository.find_by_trace_id(trace_id=trace_id)

    @Transactional()
    def get_count(self):
        return self.eyesmag_repository.get_count()

    @Transactional()
    def convert(self, trace_id: str):
        eyesmag = self.eyesmag_repository.find_by_trace_id(trace_id=trace_id)
        if eyesmag is not None:

            post = self.post_repository.find_by_trace_id(trace_id=eyesmag.trace_id)
            if post is None:
                llm_content = ContentCreator().summary(eyesmag.content)

                self.post_repository.add(post_entity=PostEntity.new(
                    trace_id=eyesmag.trace_id,
                    reference_link=eyesmag.reference_link,
                    thumbnail=eyesmag.thumbnail,
                    title=eyesmag.title,
                    content=llm_content,
                    keyword="eyesmag",
                    platform="eyesmag",
                    created_at=int(time.time())
                ))

                self.eyesmag_repository.update_on_convert(
                    trace_id=eyesmag.trace_id,
                    is_convert=CONVERT.ON.value
                )

                return {
                    "before_content": eyesmag.content,
                    "after_content": llm_content
                }

    @Transactional()
    def daily_collect(self):
        fetched_contents = self.service.fetched_data(page=1)
        fetched_contents_by_titles = []
        for fetched_content in fetched_contents:
            self.service.logging(logger=EYESMAG_USECASE_LOGGER, data=fetched_content.reference_date)
            fetched_contents_by_titles.append(fetched_content.title)

        saved_contents = self.eyesmag_repository.find_by_titles(
            titles=fetched_contents_by_titles
        )
        saved_contents_by_titles = [save_content.title for save_content in saved_contents]

        unsaved_contents_by_titles = self.service.not_exist_content_by_title(
            fetched_contents_by_titles=fetched_contents_by_titles,
            saved_contents_by_titles=saved_contents_by_titles
        )

        for unsaved_contents_by_title in unsaved_contents_by_titles:
            for eyesmags_dto in fetched_contents:
                if eyesmags_dto.title == unsaved_contents_by_title:
                    self.eyesmag_repository.add(
                        eyesmag_entity=EyesMagEntity.from_dto(eyesmags_dto)
                    )

        self.service.update_notify(count=len(unsaved_contents_by_titles))

    def all_collect(self):
        start_page = 1
        statistics = {"count": 0}

        eyesmag_dtos: List[EyesMagDto] = []

        while True:
            eyesmags_dto_list = sorted(self.service.fetched_data(page=start_page), reverse=True)
            if not eyesmags_dto_list:
                break

            if self.service.is_stop_collect(reference_date=eyesmags_dto_list[0].reference_date):
                break

            for eyesmag_dto in eyesmags_dto_list:
                self.service.logging(logger=EYESMAG_USECASE_LOGGER, data=eyesmag_dto.reference_date)
                eyesmag_dtos.append(eyesmag_dto)
            start_page += 1

        with self.session.begin():
            for eyesmags_dto in eyesmag_dtos:
                eyesmag = self.eyesmag_repository.find_by_title(title=eyesmags_dto.title)
                if eyesmag is None:
                    self.eyesmag_repository.add(
                        eyesmag_entity=EyesMagEntity.from_dto(eyesmags_dto)
                    )
                    statistics['count'] += 1
                else:
                    self.eyesmag_repository.update(
                        eyesmag_entity=EyesMagEntity.from_dto(eyesmags_dto)
                    )

        self.service.update_notify(count=statistics['count'])
