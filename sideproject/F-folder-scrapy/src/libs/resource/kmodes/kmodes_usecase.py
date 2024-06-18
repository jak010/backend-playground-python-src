from __future__ import annotations

import logging
import time
from typing import List, Optional, Dict, Tuple, Literal

from src.config.context import Transactional
from src.libs.resource.abstracts.abstract_usecase import (
    AbstractUsecase,
    AbstractUsecaseCRUDImplements,
    AbstrctUsecaseCrawlerImplements

)
from src.libs.resource.common.define import CONVERT
from src.libs.resource.common.universal_entity import UniversalEntity
from src.adapter.kmodes.api.libs.dto import KmodesDto
from src.libs.resource.kmodes.kmodes_service import KmodesService
from src.libs.resource.kmodes.kmodes_entity import KmodesEntity
from src.libs.resource.post.post_entity import PostEntity
from src.libs.utils.content_creator import ContentCreator

KMODES_USECASE_LOGGER = logging.getLogger("uvicorn.error")


class KmodesUsecase(
    AbstractUsecase,
    AbstractUsecaseCRUDImplements[UniversalEntity],
    AbstrctUsecaseCrawlerImplements
):

    def __init__(self):
        self.service = KmodesService()
        self.content_creator = ContentCreator()

    @Transactional()
    def get_content_list(self,
                         sort_key: str = None,
                         sort_type: Literal['DESC', 'ASC'] = None,
                         page: int = None,
                         item_per_page: int = None
                         ) -> Tuple[List[UniversalEntity], int]:
        return self.kmodes_repository.find_by(
            sort_key=sort_key,
            sort_type=sort_type,
            page=page,
            item_per_page=item_per_page
        )

    @Transactional()
    def get_content(self, trace_id: str) -> Optional[KmodesEntity]:
        return self.kmodes_repository.find_by_trace_id(trace_id=trace_id)

    @Transactional()
    def get_count(self) -> int:
        return self.kmodes_repository.get_count()

    @Transactional()
    def convert(self, trace_id: str) -> Dict[str, str]:
        kmodes_content = self.kmodes_repository.find_by_trace_id(trace_id=trace_id)

        if kmodes_content:
            post = self.post_repository.find_by_trace_id(trace_id=kmodes_content.trace_id)
            if post is None:
                llm_content = self.content_creator.summary(
                    kmodes_content.content + "\n\n" + kmodes_content.thumbnail
                )

                self.post_repository.add(PostEntity.new(
                    trace_id=kmodes_content.trace_id,
                    title=kmodes_content.title,
                    content=llm_content,
                    keyword="kmodes",
                    platform="kmodes",
                    thumbnail=kmodes_content.thumbnail,
                    reference_link=kmodes_content.reference_link,
                    created_at=int(time.time()),
                ))

                self.kmodes_repository.update_by_convert(
                    trace_id=kmodes_content.trace_id,
                    is_convert=CONVERT.ON
                )

                return {
                    "before_content": kmodes_content.content,
                    "after_content": llm_content
                }

    @Transactional()
    def daily_collect(self):
        start_page = 1

        fetched_urls = self.service.fetch_content_list(page=start_page)
        fetched_contents = [self.service.fetch_content(url) for url in fetched_urls]
        fetched_reference_ids = [int(fetched_content.reference_id) for fetched_content in fetched_contents]

        saved_contents = self.kmodes_repository.find_by_reference_ids(reference_ids=fetched_reference_ids)
        saved_reference_ids = [int(saved_content.reference_id) for saved_content in saved_contents]

        not_exsit_reference_ids = self.service.not_exist_reference_ids(
            fetched_reference_ids=fetched_reference_ids,
            saved_reference_ids=saved_reference_ids
        )

        for not_exsit_reference_id in not_exsit_reference_ids:
            for fetched_content in fetched_contents:
                if not_exsit_reference_id == int(fetched_content.reference_id):
                    self.kmodes_repository.add(kmodes_entity=KmodesEntity.from_dto(fetched_content))

        self.service.update_notify(count=len(not_exsit_reference_ids))

    def all_collect(self):
        kmodes_dtos: List[KmodesDto] = []
        start_page = 1
        stop_collect = True

        while stop_collect:
            fetch_content_list = self.service.fetch_content_list(page=start_page)

            for url in fetch_content_list:
                fetched_content = self.service.fetch_content(url=url)

                if self.service.is_stop_collect(self.service.to_datetime(fetched_content.reference_date)):
                    stop_collect = False
                    break

                kmodes_dtos.append(fetched_content)
                self.service.logging(logger=KMODES_USECASE_LOGGER, data=fetched_content.reference_date)

            start_page += 1

        for kmodes_dto in kmodes_dtos:
            with self.session.begin():
                kmodes_entity = self.kmodes_repository.find_by_reference_id(reference_id=kmodes_dto.reference_id)
                if kmodes_entity is None:
                    self.kmodes_repository.add(
                        kmodes_entity=KmodesEntity.from_dto(kmodes_dto=kmodes_dto)
                    )
                else:
                    self.kmodes_repository.update(
                        kmodes_entity=KmodesEntity.from_dto(kmodes_dto=kmodes_dto)
                    )

        self.service.update_notify(count=len(kmodes_dtos))
