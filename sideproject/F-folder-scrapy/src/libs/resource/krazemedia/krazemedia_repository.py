from __future__ import annotations

import uuid
from typing import List, Optional, Literal, Any, Type

from sqlalchemy import func

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.krazemedia.krazemedia_entity import KrazeMediaEntity


class KrazeMediaRepository(AbstractRepository):
    def add(self, krazemedia_entity: KrazeMediaEntity) -> KrazeMediaEntity:
        self._session.add(krazemedia_entity)
        self._session.flush()
        return krazemedia_entity

    def update(self, krazemedia_entity: KrazeMediaEntity) -> KrazeMediaEntity:
        self._session.query(KrazeMediaEntity).filter(
            KrazeMediaEntity.trace_id == krazemedia_entity.trace_id
        ).update({
            KrazeMediaEntity.reference_id: krazemedia_entity.reference_id,
            KrazeMediaEntity.reference_date: krazemedia_entity.reference_date,
            KrazeMediaEntity.reference_link: krazemedia_entity.reference_link,
            KrazeMediaEntity.thumbnail: krazemedia_entity.thumbnail,
            KrazeMediaEntity.title: krazemedia_entity.title,
            KrazeMediaEntity.content: krazemedia_entity.content,
        })
        return krazemedia_entity

    def update_by_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        self._session.query(KrazeMediaEntity).filter(
            KrazeMediaEntity.trace_id == trace_id
        ).update({KrazeMediaEntity.is_convert: is_convert})

    def find_by(
            self,
            page: int,
            item_per_page: int,
            sort_key: str,
            sort_type: Literal["DESC", "ASC"],
    ) -> tuple[List[KrazeMediaEntity], Any]:
        query = self._session.query(KrazeMediaEntity) \
            .order_by(sort_key, "id") \
            .limit(item_per_page) \
            .offset(self.get_page_limit(page, item_per_page))

        count_query = self._session.query(func.count(KrazeMediaEntity.id))

        return query.all(), count_query.scalar()

    def find_by_trace_id(self, trace_id: str) -> KrazeMediaEntity:
        query = self._session.query(KrazeMediaEntity).filter(KrazeMediaEntity.trace_id == trace_id)
        return query.one_or_none()

    def find_by_reference_id(self, reference_id: int) -> Optional[KrazeMediaEntity]:
        query = self._session.query(KrazeMediaEntity).where(KrazeMediaEntity.reference_id == reference_id)
        return query.one_or_none()

    def find_by_titles(self, titles: List[str]) -> List[KrazeMediaEntity]:
        query = self._session.query(KrazeMediaEntity).where(KrazeMediaEntity.title.in_(titles))
        return query.all()
