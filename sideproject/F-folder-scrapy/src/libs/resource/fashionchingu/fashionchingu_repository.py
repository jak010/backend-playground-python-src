from __future__ import annotations

import uuid
from typing import List, Optional, Tuple

from sqlalchemy import func

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.fashionchingu.fashiochingu_entity import FashionChinguEntity


class FashionChinguRepository(AbstractRepository):
  
    def add(self, fashionchingu_entity: FashionChinguEntity):
        self._session.add(fashionchingu_entity)
        self._session.flush()

    def update(self, fashionchingu_entity: FashionChinguEntity) -> FashionChinguEntity:
        self._session.query(FashionChinguEntity).filter(
            FashionChinguEntity.trace_id == fashionchingu_entity.trace_id
        ).update({
            FashionChinguEntity.reference_id: fashionchingu_entity.reference_id,
            FashionChinguEntity.reference_date: fashionchingu_entity.reference_date,
            FashionChinguEntity.reference_link: fashionchingu_entity.reference_link,
            FashionChinguEntity.thumbnail: fashionchingu_entity.thumbnail,
            FashionChinguEntity.title: fashionchingu_entity.title,
            FashionChinguEntity.content: fashionchingu_entity.content,
        })
        return fashionchingu_entity

    def update_on_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        self._session.query(FashionChinguEntity).filter(
            FashionChinguEntity.trace_id == trace_id
        ).update({FashionChinguEntity.is_convert: is_convert})

    def find_by(self,
                sort_key,
                sort_type,
                page,
                item_per_page
                ) -> Tuple[List[FashionChinguEntity], int]:
        query = self._session.query(FashionChinguEntity) \
            .order_by(sort_key, "id") \
            .limit(item_per_page) \
            .offset(self.get_page_limit(page, item_per_page))

        count_query = self._session.query(func.count(FashionChinguEntity.id))

        return query.all(), count_query.scalar()

    def find_by_trace_id(self, trace_id: str) -> FashionChinguEntity:
        query = self._session.query(FashionChinguEntity) \
            .filter(FashionChinguEntity.trace_id == trace_id)

        result = query.one_or_none()

        if result:
            return result

    def find_by_title(self, title: str) -> Optional[FashionChinguEntity]:
        query = self._session.query(FashionChinguEntity) \
            .filter(FashionChinguEntity.title == title)

        result = query.one_or_none()

        if result:
            return result

    def find_by_titles(self, titles: List[str]) -> List[FashionChinguEntity]:
        query = self._session.query(FashionChinguEntity) \
            .filter(FashionChinguEntity.title.in_(titles))

        return query.all()
