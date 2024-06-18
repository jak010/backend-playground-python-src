from __future__ import annotations

import uuid
from typing import List, Optional, Literal, Any, Type

from sqlalchemy import func

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.kmodes.kmodes_entity import KmodesEntity


class KmodesRepository(AbstractRepository):

    def add(self, kmodes_entity: KmodesEntity) -> KmodesEntity:
        self._session.add(kmodes_entity)
        self._session.flush()
        return kmodes_entity

    def update(self, kmodes_entity: KmodesEntity) -> KmodesEntity:
        self._session.query(KmodesEntity).filter(
            KmodesEntity.reference_id == kmodes_entity.reference_id
        ).update({
            KmodesEntity.reference_date: kmodes_entity.reference_date,
            KmodesEntity.reference_link: kmodes_entity.reference_link,
            KmodesEntity.thumbnail: kmodes_entity.thumbnail,
            KmodesEntity.title: kmodes_entity.title,
            KmodesEntity.content: kmodes_entity.content,
        })

        return kmodes_entity

    def update_by_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        self._session.query(KmodesEntity).filter(
            KmodesEntity.trace_id == trace_id
        ).update({KmodesEntity.is_convert: is_convert})

    def find_by(
            self,
            page: int,
            item_per_page: int,
            sort_key: str,
            sort_type: Literal["DESC", "ASC"],
    ) -> tuple[List[KmodesEntity], Any]:
        query = self._session.query(KmodesEntity) \
            .order_by(sort_key, "id") \
            .limit(item_per_page) \
            .offset(self.get_page_limit(page, item_per_page))

        count_query = self._session.query(func.count(KmodesEntity.id))

        return query.all(), count_query.scalar()

    def find_by_trace_id(self, trace_id: str) -> KmodesEntity:
        query = self._session.query(KmodesEntity).filter(KmodesEntity.trace_id == trace_id)
        return query.one_or_none()

    def find_by_reference_id(self, reference_id: int) -> Optional[KmodesEntity]:
        query = self._session.query(KmodesEntity).where(KmodesEntity.reference_id == reference_id)
        return query.one_or_none()

    def find_by_reference_ids(self, reference_ids: list[int]) -> List[Type[KmodesEntity]]:
        query = self._session.query(KmodesEntity).where(KmodesEntity.reference_id.in_(reference_ids))
        return query.all()
