from __future__ import annotations

import time
from typing import List, Tuple

from sqlalchemy import desc, asc, func, and_

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.post.post_entity import PostEntity
from src.libs.utils import time_utils


class PostRepository(AbstractRepository):

    def add(self, post_entity: PostEntity):
        self._session.add(post_entity)
        self._session.flush()

    def update(self, post_entity: PostEntity):
        ...

    def update_by(self, trace_id, title, content, keyword, is_deleted):
        kwargs = {}
        if title is not None:
            kwargs[PostEntity.title] = title
        if content is not None:
            kwargs[PostEntity.content] = content
        if keyword is not None:
            kwargs[PostEntity.keyword] = keyword
        if is_deleted is not None:
            kwargs[PostEntity.is_deleted] = is_deleted
        kwargs[PostEntity.modified_at] = int(time.time())

        self._session.query(PostEntity).filter(PostEntity.trace_id == trace_id).update(kwargs)
        self._session.flush()

    def find_by(
            self,
            keyword: str = None,
            platform: str = None,
            content: str = None,
            page: int = None,
            item_per_page: int = None,
            sort_key: str = None,
            sort_type: str = None
    ) -> Tuple[List[PostEntity], int]:

        query = self._session.query(PostEntity)
        count_query = self._session.query(func.count(PostEntity.post_id))

        # condition
        if platform is not None:
            query = query.filter(PostEntity.platform == platform)
            count_query = count_query.filter(PostEntity.platform == platform)
        if keyword is not None:
            query = query.filter(PostEntity.keyword == keyword)
            count_query = count_query.filter(PostEntity.keyword == keyword)
        if content is not None:
            content = "%{}%".format(content)
            query = query.filter(PostEntity.content.like(content))
            count_query = count_query.filter(PostEntity.content.like(content))
        query = query.filter(
            and_(
                PostEntity.created_at >= time_utils.midnight_kst(),
                PostEntity.created_at <= time_utils.midnight_kst() + 86400
            ))
        count_query = count_query.filter(
            and_(
                PostEntity.created_at >= time_utils.midnight_kst(),
                PostEntity.created_at <= time_utils.midnight_kst() + 86400
            ))

        # sort
        if sort_type == "DESC":
            query = query.order_by(desc(sort_key), PostEntity.post_id)
        if sort_type == "ASC":
            query = query.order_by(asc(sort_key), PostEntity.post_id)

        # paginate
        query = query.limit(item_per_page).offset((page - 1) * item_per_page)

        return query.all(), count_query.scalar()

    def find_by_trace_id(self, trace_id) -> PostEntity:
        query = self._session.query(PostEntity).filter(PostEntity.trace_id == trace_id)
        return query.one_or_none()

    def get_count(self):
        query = self._session.query(PostEntity.post_id)
        return query.count()

    def get_today_created_content(self):
        query = self._session.query(func.count(PostEntity.post_id)) \
            .filter(PostEntity.created_at >= time_utils.midnight_kst()) \
            .filter(PostEntity.created_at <= time_utils.midnight_kst() + 86400)

        return query.scalar()

    def increase_views(self, post_entity: PostEntity):
        self._session.query(PostEntity) \
            .filter(PostEntity.trace_id == post_entity.trace_id) \
            .update({PostEntity.views: post_entity.views + 1})
