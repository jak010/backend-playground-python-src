from __future__ import annotations

import datetime
from typing import Optional, List

from sqlalchemy import desc

from src.app.domain.abstract import AbstractRepository
from src.app.domain.auditions import AuditionEntity


class AuditionRepository(AbstractRepository[AuditionEntity]):

    def get_by_categories(self, categories: list[str], submissions: List[int], page: int = 1, item_per_page: int = 10) -> List[AuditionEntity]:
        query = self.session.query(AuditionEntity) \
            .filter(AuditionEntity.category.in_(categories)) \
            .filter(AuditionEntity.is_remake == 1) \
            .filter(AuditionEntity.end_date >= datetime.datetime.now())

        if submissions:
            query = query.filter(AuditionEntity.id.not_in(submissions))

        query = query.order_by(desc(AuditionEntity.end_date))
        query = query.limit(item_per_page).offset((page - 1) * item_per_page)
        return query.all()

    def get_by_id(self, audition_id: int) -> Optional[AuditionEntity]:
        return self.session.query(AuditionEntity) \
            .filter(AuditionEntity.id == audition_id) \
            .filter(AuditionEntity.end_date >= datetime.datetime.now()) \
            .one_or_none()
