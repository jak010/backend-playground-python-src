from __future__ import annotations

from typing import List, Tuple

from fastapi import Request

from src.config.context import Transactional
from src.libs.resource.abstracts.abstract_usecase import AbstractUsecase, AbstractUsecaseCRUDImplements
from src.libs.resource.post.post_entity import PostEntity
from src.libs.resource.post.post_history_entity import PostHistoryEntity


class PostUsecase(AbstractUsecase, AbstractUsecaseCRUDImplements[PostEntity]):

    @Transactional()
    def get_content_list(
            self,
            keyword: str = None,
            platform: str = None,
            content: str = None,
            page: int = None,
            item_per_page: int = None,
            sort_key: str = None,
            sort_type: str = None
    ) -> Tuple[List[PostEntity], int]:
        return self.post_repository.find_by(
            keyword=keyword,
            platform=platform,
            content=content,
            page=page,
            item_per_page=item_per_page,
            sort_key=sort_key,
            sort_type=sort_type,
        )

    @Transactional()
    def get_count(self) -> int:
        return self.post_repository.get_count()

    @Transactional()
    def get_content(self, trace_id: str, request: Request):
        post = self.post_repository.find_by_trace_id(trace_id=trace_id)
        if post:
            self.post_history_repository.add(
                post_history_entity=PostHistoryEntity.new(post_id=post.post_id, request=request)
            )

            self.post_repository.increase_views(post_entity=post)
            return post

    @Transactional()
    def get_created_today_content(self):
        return self.post_repository.get_today_created_content()

    @Transactional()
    def update_by(
            self,
            trace_id: str,
            title: str = None,
            content: str = None,
            keyword: str = None,
            is_deleted: bool = None
    ):
        return self.post_repository.update_by(
            trace_id=trace_id,
            title=title,
            content=content,
            keyword=keyword,
            is_deleted=is_deleted
        )
