from __future__ import annotations

import time
from typing import Optional, Dict, List

from src.config.context import Transactional
from src.libs.resource.abstracts.abstract_usecase import (
    AbstractUsecase,
    AbstractUsecaseCRUDImplements,
    AbstrctUsecaseCrawlerImplements, T
)
from src.libs.resource.common.define import CONVERT
from src.libs.resource.post.post_entity import PostEntity
from src.libs.resource.unnielooks.unnielooks_service import UnnieLooksService
from src.libs.utils.content_creator import ContentCreator


class UnnieLooksUsecase(
    AbstractUsecase,
    AbstractUsecaseCRUDImplements,
    AbstrctUsecaseCrawlerImplements
):

    def __init__(self):
        self.service = UnnieLooksService()

    @Transactional()
    def get_content_list(
            self,
            sort_key: str,
            sort_type: str,
            page: int,
            item_per_page: int
    ):
        return self.unnielooks_repository.find_by(
            sort_key=sort_key,
            sort_type=sort_type,
            page=page,
            item_per_page=item_per_page
        )

    @Transactional()
    def get_count(self):
        return self.unnielooks_repository.get_count()

    @Transactional()
    def get_content(self, trace_id: str) -> Optional[T]:
        return self.unnielooks_repository.find_by_trace_id(trace_id=trace_id)

    @Transactional()
    def convert(self, trace_id: str) -> Dict[str, str]:
        unnielooks = self.unnielooks_repository.find_by_trace_id(trace_id=trace_id)
        if unnielooks is not None:
            post = self.post_repository.find_by_trace_id(trace_id=unnielooks.trace_id)
            if post is None:
                llm_content = ContentCreator().summary(unnielooks.content)

                self.post_repository.add(PostEntity.new(
                    trace_id=unnielooks.trace_id,
                    reference_link=unnielooks.reference_link,
                    thumbnail=unnielooks.thumbnail,
                    title=unnielooks.title,
                    content=llm_content,
                    keyword="unnielooks",
                    platform="unnielooks",
                    created_at=int(time.time())
                ))

                self.unnielooks_repository.update_on_convert(
                    trace_id=unnielooks.trace_id,
                    is_convert=CONVERT.ON
                )

                return {
                    "before_content": unnielooks.content,
                    "after_content": llm_content
                }

    @Transactional()
    def daily_collect(self):
        start_page = 1

        fetched_content_links = self.service.fetch_links(page=start_page)
        fetched_contents = [self.service.fetch_content(link) for link in fetched_content_links]
        fetched_contents_by_titles = [str(fetched_content.title) for fetched_content in fetched_contents]

        saved_contents = self.unnielooks_repository.find_by_titles(titles=fetched_contents_by_titles)
        saved_contents_by_titles = [str(saved_content.title) for saved_content in saved_contents]

        not_exist_contents_by_titles = self.service.not_exist_content_by_titles(
            fetched_contents_titles=fetched_contents_by_titles,
            saved_contents_titles=saved_contents_by_titles
        )

        from src.libs.resource.unnielooks.unnielooks_entity import UnnielooksEntity

        for not_exist_contents_by_title in not_exist_contents_by_titles:
            for unnielooks_dto in fetched_contents:
                if str(not_exist_contents_by_title) == str(unnielooks_dto.title):
                    self.unnielooks_repository.add(unnielooks_entity=UnnielooksEntity.from_dto(unnielooks_dto))

        self.service.update_notify(count=len(not_exist_contents_by_titles))

    def all_collect(self):
        from src.adapter.unnielooks.api.libs.dto import UnnieLooksDto
        from src.libs.resource.unnielooks.unnielooks_entity import UnnielooksEntity
        unsaved_contents: List[UnnieLooksDto] = []

        start_page = 1
        is_stop = False

        while True:
            if is_stop:
                break

            fetched_content_links = self.service.fetch_links(page=start_page)
            for fetched_content_link in fetched_content_links:
                fetch_content = self.service.fetch_content(fetched_content_link)
                self.service.logging(fetch_content.reference_date)
                if self.service.is_stop_collect(fetch_content.reference_date):
                    is_stop = True
                    break

                unsaved_contents.append(fetch_content)
            start_page += 1

        with self.session.begin():
            for unsaved_content in unsaved_contents:
                unnielooks_entity = self.unnielooks_repository.find_by_title(unsaved_content.title)
                if unnielooks_entity is None:
                    self.unnielooks_repository.add(
                        unnielooks_entity=UnnielooksEntity.from_dto(unnielooks_dto=unsaved_content)
                    )

        self.service.update_notify(count=len(unsaved_contents))
