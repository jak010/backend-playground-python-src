from __future__ import annotations

import uuid
from typing import List, Optional, Literal, Any, Type

from sqlalchemy import func

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.krazefashion.krazefashion_entity import KrazeFashionEntity


class KrazeFashionRepository(AbstractRepository):
    def add(self, krazefashion_entity: KrazeFashionEntity) -> KrazeFashionEntity:
        self._session.add(krazefashion_entity)
        self._session.flush()
        return krazefashion_entity

    def update(self, krazefashion_entity: KrazeFashionEntity) -> KrazeFashionEntity:
        self._session.query(KrazeFashionEntity).filter(
            KrazeFashionEntity.trace_id == krazefashion_entity.trace_id
        ).update({
            KrazeFashionEntity.reference_id: krazefashion_entity.reference_id,
            KrazeFashionEntity.reference_date: krazefashion_entity.reference_date,
            KrazeFashionEntity.reference_link: krazefashion_entity.reference_link,
            KrazeFashionEntity.thumbnail: krazefashion_entity.thumbnail,
            KrazeFashionEntity.title: krazefashion_entity.title,
            KrazeFashionEntity.content: krazefashion_entity.content,
        })
        return krazefashion_entity

    def update_by_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        self._session.query(KrazeFashionEntity).filter(
            KrazeFashionEntity.trace_id == trace_id
        ).update({KrazeFashionEntity.is_convert: is_convert})

    def find_by(
            self,
            page: int,
            item_per_page: int,
            sort_key: str,
            sort_type: Literal["DESC", "ASC"],
    ) -> tuple[List[KrazeFashionEntity], Any]:
        query = self._session.query(KrazeFashionEntity) \
            .order_by(sort_key, "id") \
            .limit(item_per_page) \
            .offset(self.get_page_limit(page, item_per_page))

        count_query = self._session.query(func.count(KrazeFashionEntity.id))

        return query.all(), count_query.scalar()

    def find_by_trace_id(self, trace_id: str) -> KrazeFashionEntity:
        query = self._session.query(KrazeFashionEntity).filter(KrazeFashionEntity.trace_id == trace_id)
        return query.one_or_none()

    def find_by_reference_id(self, reference_id: int) -> Optional[KrazeFashionEntity]:
        query = self._session.query(KrazeFashionEntity).where(KrazeFashionEntity.reference_id == reference_id)
        return query.one_or_none()

    def find_by_titles(self, titles: List[str]) -> List[KrazeFashionEntity]:
        query = self._session.query(KrazeFashionEntity).where(KrazeFashionEntity.title.in_(titles))
        return query.all()
