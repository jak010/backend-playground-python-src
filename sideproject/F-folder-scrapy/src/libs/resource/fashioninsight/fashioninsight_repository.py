from __future__ import annotations

import uuid
from typing import Optional, List, Tuple

from sqlalchemy import desc, asc, func

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.fashioninsight.fashioninsight_entity import FashionInsightEntity


class FashionInsightRepository(AbstractRepository):
    TABLE_NAME = "fashioninsight"

    def add(self, fashioninsight_entity: FashionInsightEntity):
        self._session.add(fashioninsight_entity)
        self._session.flush()

    def update(self, *args, **kwargs):
        pass

    def update_on_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        self._session.query(FashionInsightEntity).filter(
            FashionInsightEntity.trace_id == trace_id
        ).update({FashionInsightEntity.is_convert: is_convert})

    def find_by(self,
                sort_key: str = None,
                sort_type: str = None,
                page: int = None,
                item_per_page: int = None,
                ) -> Tuple[List[UniversalEntity], int]:

        query = self._session.query(FashionInsightEntity)
        count_query = self._session.query(func.count(FashionInsightEntity.id))

        # sort
        if sort_type == 'DESC':
            query = query.order_by(desc(sort_key), FashionInsightEntity.id)
        if sort_type == 'ASC':
            query = query.order_by(asc(sort_key), FashionInsightEntity.id)

        # paginate
        query = query.limit(item_per_page) \
            .offset(self.get_page_limit(page, item_per_page))

        return query.all(), count_query.scalar()

    def find_by_reference_id(self, refernce_id: int) -> FashionInsightEntity:
        query = self._session.query(FashionInsightEntity.reference_id) \
            .filter(FashionInsightEntity.reference_id == refernce_id)

        result = query.one_or_none()
        if result:
            return result

    def find_by_reference_ids(self, reference_ids: list[int]) -> List[FashionInsightEntity]:
        query = self._session.query(FashionInsightEntity) \
            .filter(FashionInsightEntity.reference_id.in_(reference_ids))
        return query.all()

    def find_by_trace_id(self, trace_id: str) -> Optional[FashionInsightEntity]:
        query = self._session.query(FashionInsightEntity) \
            .filter(FashionInsightEntity.trace_id == trace_id)

        result = query.one_or_none()

        if result:
            return result
