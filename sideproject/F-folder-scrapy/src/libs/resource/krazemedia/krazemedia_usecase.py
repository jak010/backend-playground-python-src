from __future__ import annotations

import logging
import time
from typing import List, Optional, Dict, Tuple, Literal

from src.adapter import slack
from src.config.context import Transactional
from src.libs.resource.abstracts.abstract_usecase import (
    AbstractUsecase,
    AbstractUsecaseCRUDImplements,
    AbstrctUsecaseCrawlerImplements

)
from src.libs.resource.common.define import CONVERT
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.krazemedia.krazemedia_entity import KrazeMediaEntity
from src.libs.resource.krazemedia.krazemedia_service import KrazeMediaService
from src.libs.resource.post.post_entity import PostEntity
from src.libs.utils.content_creator import ContentCreator

KRAZEMEDIA_USECASE_LOGGER = logging.getLogger("uvicorn.error")


class KrazeMediaUsecase(
    AbstractUsecase,
    AbstractUsecaseCRUDImplements[UniversalEntity],
    AbstrctUsecaseCrawlerImplements
):

    def __init__(self):
        self.service = KrazeMediaService()
        self.content_creator = ContentCreator()

    @Transactional()
    def get_content_list(self,
                         sort_key: str = None,
                         sort_type: Literal['DESC', 'ASC'] = None,
                         page: int = None,
                         item_per_page: int = None
                         ) -> Tuple[List[UniversalEntity], int]:
        return self.krazemedia_repository.find_by(
            sort_key=sort_key,
            sort_type=sort_type,
            page=page,
            item_per_page=item_per_page
        )

    @Transactional()
    def get_content(self, trace_id: str):
        return self.krazemedia_repository.find_by_trace_id(trace_id=trace_id)

    @Transactional()
    def get_count(self) -> int:
        return self.krazemedia_repository.get_count()

    @Transactional()
    def convert(self, trace_id: str) -> Dict[str, str]:
        krazemedia = self.krazemedia_repository.find_by_trace_id(trace_id=trace_id)

        if krazemedia:
            post = self.post_repository.find_by_trace_id(trace_id=krazemedia.trace_id)

            if post is None:
                llm_content = self.content_creator.summary(krazemedia.content)

                self.post_repository.add(PostEntity.new(
                    trace_id=krazemedia.trace_id,
                    reference_link=krazemedia.reference_link,
                    thumbnail=krazemedia.thumbnail,
                    title=krazemedia.title,
                    content=llm_content,
                    keyword="krazemedia",
                    platform="krazemedia",
                    created_at=int(time.time())
                ))

                self.krazemedia_repository.update_by_convert(
                    trace_id=krazemedia.trace_id,
                    is_convert=CONVERT.ON.value
                )

                return {
                    "before_content": krazemedia.content,
                    "after_content": llm_content
                }

    @Transactional()
    def daily_collect(self):
        krdrama_list = self.service.fetch_kdrama_content_list()
        tvmovies_list = self.service.fetch_tvmovies_content_list()
        fetched_urls = krdrama_list + tvmovies_list

        fetched_contents = [self.service.fetch_content(url) for url in fetched_urls]
        fetched_titles = []
        for fetched_content in fetched_contents:
            fetched_titles.append(fetched_content.title)

        saved_contents = self.krazemedia_repository.find_by_titles(titles=fetched_titles)
        saved_titles = [saved_content.title for saved_content in saved_contents]

        not_exsit_titles = self.service.not_exist_titles(fetched_titles=fetched_titles, saved_titles=saved_titles)

        for fetched_content in fetched_contents:
            if fetched_content.title in not_exsit_titles:
                self.krazemedia_repository.add(krazemedia_entity=KrazeMediaEntity.from_dto(fetched_content))

        self.service.update_notify(count=len(not_exsit_titles))

    def all_collect(self):
        krdrama_list = self.service.fetch_kdrama_content_list()
        tvmovies_list = self.service.fetch_tvmovies_content_list()
        fetched_urls = krdrama_list + tvmovies_list

        fetched_contents = [self.service.fetch_content(url) for url in fetched_urls]
        fetched_titles = []
        for fetched_content in fetched_contents:
            self.service.logging(logger=KRAZEMEDIA_USECASE_LOGGER, data=fetched_content.reference_date)
            fetched_titles.append(fetched_content.title)

        with self.session.begin():
            saved_contents = self.krazemedia_repository.find_by_titles(titles=fetched_titles)
            saved_titles = [saved_content.title for saved_content in saved_contents]

            not_exsit_titles = self.service.not_exist_titles(fetched_titles=fetched_titles, saved_titles=saved_titles)

            for fetched_content in fetched_contents:
                if fetched_content.title in not_exsit_titles:
                    self.krazemedia_repository.add(krazemedia_entity=KrazeMediaEntity.from_dto(fetched_content))

        self.service.update_notify(count=len(not_exsit_titles))
