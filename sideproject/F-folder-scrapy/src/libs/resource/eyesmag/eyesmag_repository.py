from __future__ import annotations

import uuid
from typing import List, Optional, Tuple

from sqlalchemy import func

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.eyesmag.eyesmag_entity import EyesMagEntity


class EyesMagRepository(AbstractRepository):

    def add(self, eyesmag_entity: EyesMagEntity):
        self._session.add(eyesmag_entity)
        self._session.flush()

    def update(self, eyesmag_entity: EyesMagEntity):
        self._session.query(EyesMagEntity).filter(
            EyesMagEntity.trace_id == eyesmag_entity.trace_id
        ).update({
            EyesMagEntity.reference_id: eyesmag_entity.reference_id,
            EyesMagEntity.reference_date: eyesmag_entity.reference_date,
            EyesMagEntity.reference_link: eyesmag_entity.reference_link,
            EyesMagEntity.thumbnail: eyesmag_entity.thumbnail,
            EyesMagEntity.title: eyesmag_entity.title,
            EyesMagEntity.content: eyesmag_entity.content,
        })
        return eyesmag_entity

    def update_on_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        self._session.query(EyesMagEntity).filter(
            EyesMagEntity.trace_id == trace_id
        ).update({EyesMagEntity.is_convert: is_convert})

    def find_by(
            self,
            sort_key: str = None,
            sort_type: str = None,
            page: int = None,
            item_per_page: int = None,
    ) -> Tuple[List[UniversalEntity], int]:
        query = self._session.query(EyesMagEntity) \
            .order_by(sort_key, "id") \
            .limit(item_per_page) \
            .offset(self.get_page_limit(page, item_per_page))

        count_query = self._session.query(func.count(EyesMagEntity.id))

        return query.all(), count_query.scalar()

    def find_by_trace_id(self, trace_id: str) -> EyesMagEntity:
        query = self._session.query(EyesMagEntity) \
            .filter(EyesMagEntity.trace_id == trace_id)
        return query.scalar()

    def find_by_title(self, title: str) -> Optional[EyesMagEntity]:
        query = self._session.query(EyesMagEntity) \
            .filter(EyesMagEntity.title == title)
        return query.scalar()

    def find_by_titles(self, titles: list[str]) -> Optional[List[EyesMagEntity]]:
        query = self._session.query(EyesMagEntity) \
            .filter(EyesMagEntity.title.in_(titles))
        return query.all()

    def find_by_reference_ids(self, reference_ids: list[int]) -> List[EyesMagEntity]:
        query = self._session.query(EyesMagEntity) \
            .filter(EyesMagEntity.reference_id.in_(reference_ids))
        return query.all()
