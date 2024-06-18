from __future__ import annotations

import logging
import time
from typing import List, Optional, Dict, Tuple, Literal

from src.adapter.voguekorea.api.libs.dto import VogueKoreaDto
from src.config.context import Transactional
from src.libs.resource.abstracts.abstract_usecase import (
    AbstractUsecase,
    AbstractUsecaseCRUDImplements,
    AbstrctUsecaseCrawlerImplements
)
from src.libs.resource.common.define import CONVERT
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.post.post_entity import PostEntity
from src.libs.resource.voguekorea.voguekorea_entity import VogueKoreaEntity
from src.libs.resource.voguekorea.voguekorea_service import VogueKoreaService
from src.libs.utils.content_creator import ContentCreator

VOGUEKOREA_USECASE_LOGGER = logging.getLogger("uvicorn.error")


class VogueKoreaUsecase(
    AbstractUsecase,
    AbstractUsecaseCRUDImplements[VogueKoreaEntity],
    AbstrctUsecaseCrawlerImplements
):

    def __init__(self):
        self.service = VogueKoreaService()
        self.content_creator = ContentCreator()

    @Transactional()
    def get_content_list(self,
                         sort_key: str = None,
                         sort_type: Literal['DESC', 'ASC'] = None,
                         page: int = None,
                         item_per_page: int = None
                         ) -> Tuple[List[UniversalEntity], int]:
        return self.voguekorea_repository.find_by(
            sort_key=sort_key,
            sort_type=sort_type,
            page=page,
            item_per_page=item_per_page
        )

    @Transactional()
    def get_content(self, trace_id: str) -> Optional[VogueKoreaEntity]:
        return self.voguekorea_repository.find_by_trace_id(trace_id)

    @Transactional()
    def get_count(self):
        return self.voguekorea_repository.get_count()

    @Transactional()
    def convert(self, trace_id: str) -> Dict[str, str]:
        if voguekorea := self.voguekorea_repository.find_by_trace_id(trace_id=trace_id):
            post = self.post_repository.find_by_trace_id(trace_id=voguekorea.trace_id)

            if post is None:
                llm_content = self.content_creator.summary(voguekorea.content)

                self.post_repository.add(PostEntity.new(
                    trace_id=voguekorea.trace_id,
                    reference_link=voguekorea.reference_link,
                    thumbnail=voguekorea.thumbnail,
                    title=voguekorea.title,
                    content=llm_content,
                    keyword="voguekorea",
                    platform="voguekorea",
                    created_at=int(time.time())
                ))

                self.voguekorea_repository.update_by_convert(
                    trace_id=voguekorea.trace_id,
                    is_convert=CONVERT.ON
                )

                return {
                    "before_content": voguekorea.content,
                    "after_content": llm_content
                }

    @Transactional()
    def daily_collect(self):
        fetched_contents = self.service.fetch_contents(page=1, item_per_page=10)
        saved_contents = self.voguekorea_repository.find_by_reference_ids(
            reference_ids=self.service.get_post_ids(fetch_contents=fetched_contents)
        )

        unsaved_by_reference_ids = self.service.not_exist_refernce_ids(
            fetched_conetents_ids=self.service.get_post_ids(fetch_contents=fetched_contents),
            save_contents_ids=[int(saved_content.reference_id) for saved_content in saved_contents]
        )

        for unsaved_by_reference_id in unsaved_by_reference_ids:
            for fetch_content in fetched_contents:
                if int(fetch_content.reference_id) == int(unsaved_by_reference_id):
                    self.voguekorea_repository.add(voguekorea_entity=VogueKoreaEntity.from_dto(fetch_content))

        self.service.update_notify(count=len(unsaved_by_reference_ids))

    def all_collect(self):
        start_page = 1
        stop_year = 2022

        voguekorea_dtos: List[VogueKoreaDto] = []
        while True:
            fetched_contents = sorted(self.service.fetch_contents(page=start_page, item_per_page=20), reverse=True)

            first_content = self.service.to_datetime(reference_date=fetched_contents[0].reference_date)
            if first_content.year == stop_year:
                break

        for fetched_content in fetched_contents:
            voguekorea_dtos.append(fetched_content)
            self.service.logging(logger=VOGUEKOREA_USECASE_LOGGER, data=fetched_content.reference_date)

        start_page += 1
        with self.session.begin():
            for voguekorea_dto in voguekorea_dtos:
                voguekorea_entity = self.voguekorea_repository.find_by_reference_id(
                    reference_id=voguekorea_dto.reference_id
                )
                if voguekorea_entity is None:
                    self.voguekorea_repository.add(
                        voguekorea_entity=VogueKoreaEntity.from_dto(voguekorea_dto=voguekorea_dto)
                    )
                if voguekorea_entity is not None:
                    self.voguekorea_repository.update(
                        voguekorea_entity=VogueKoreaEntity.from_dto(voguekorea_dto=voguekorea_dto)
                    )

            self.service.update_notify(count=len(voguekorea_dtos))
