from __future__ import annotations

import uuid
from typing import List, Optional, Literal, Any, Type

from sqlalchemy import func

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.voguekorea.voguekorea_entity import VogueKoreaEntity


class VogueKoreaRepository(AbstractRepository):
    def add(self, voguekorea_entity: VogueKoreaEntity) -> VogueKoreaEntity:
        self._session.add(voguekorea_entity)
        self._session.flush()
        return voguekorea_entity

    def update(self, voguekorea_entity: VogueKoreaEntity) -> VogueKoreaEntity:
        self._session.query(VogueKoreaEntity).filter(
            VogueKoreaEntity.trace_id == voguekorea_entity.trace_id
        ).update({
            VogueKoreaEntity.reference_date: voguekorea_entity.reference_date,
            VogueKoreaEntity.reference_link: voguekorea_entity.reference_link,
            VogueKoreaEntity.thumbnail: voguekorea_entity.thumbnail,
            VogueKoreaEntity.title: voguekorea_entity.title,
            VogueKoreaEntity.content: voguekorea_entity.content,
        })
        return voguekorea_entity

    def update_by_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        self._session.query(VogueKoreaEntity).filter(
            VogueKoreaEntity.trace_id == trace_id
        ).update({VogueKoreaEntity.is_convert: is_convert})

    def find_by(
            self,
            page: int,
            item_per_page: int,
            sort_key: str,
            sort_type: Literal["DESC", "ASC"],
    ) -> tuple[List[VogueKoreaEntity], Any]:
        query = self._session.query(VogueKoreaEntity) \
            .order_by(sort_key, "id") \
            .limit(item_per_page) \
            .offset(self.get_page_limit(page, item_per_page))

        count_query = self._session.query(func.count(VogueKoreaEntity.id))
        return query.all(), count_query.scalar()

    def find_by_trace_id(self, trace_id: str) -> VogueKoreaEntity:
        query = self._session.query(VogueKoreaEntity).filter(VogueKoreaEntity.trace_id == trace_id)
        return query.one_or_none()

    def find_by_reference_id(self, reference_id: int) -> Optional[VogueKoreaEntity]:
        query = self._session.query(VogueKoreaEntity).where(VogueKoreaEntity.reference_id == reference_id)
        return query.one_or_none()

    def find_by_reference_ids(self, reference_ids: list[int]) -> List[Type[VogueKoreaEntity]]:
        query = self._session.query(VogueKoreaEntity).where(VogueKoreaEntity.reference_id.in_(reference_ids))
        return query.all()
