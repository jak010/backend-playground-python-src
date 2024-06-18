from __future__ import annotations

import uuid
from typing import List, Optional, Tuple

from sqlalchemy import func

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.unnielooks.unnielooks_entity import UnnielooksEntity


class UnnieLooksRepository(AbstractRepository):

    def add(self, unnielooks_entity: UnnielooksEntity) -> UnnielooksEntity:
        self._session.add(unnielooks_entity)
        self._session.flush()
        return unnielooks_entity

    def update(self, *args, **kwargs):
        pass

    def update_on_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        self._session.query(UnnielooksEntity).filter(
            UnnielooksEntity.trace_id == trace_id
        ).update({UnnielooksEntity.is_convert: is_convert})

    def find_by(self,
                sort_key,
                sort_type,
                page,
                item_per_page
                ) -> Tuple[List[UniversalEntity], int]:
        query = self._session.query(UnnielooksEntity) \
            .order_by(sort_key, "id") \
            .limit(item_per_page) \
            .offset(self.get_page_limit(page, item_per_page))

        count_query = self._session.query(func.count(UnnielooksEntity.id))

        return query.all(), count_query.scalar()

    def find_by_trace_id(self, trace_id: str) -> Optional[UnnielooksEntity]:
        query = self._session.query(UnnielooksEntity) \
            .filter(UnnielooksEntity.trace_id == trace_id)
        return query.one_or_none()

    def find_by_titles(self, titles: list[str]) -> Optional[List[UnnielooksEntity]]:
        query = self._session.query(UnnielooksEntity) \
            .filter(UnnielooksEntity.title.in_(titles))
        return query.all()

    def find_by_title(self, title: str) -> Optional[UnnielooksEntity]:
        query = self._session.query(UnnielooksEntity) \
            .filter(UnnielooksEntity.title == title)
        return query.one_or_none()
