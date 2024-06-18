from __future__ import annotations

from typing import List

from src.app.domain.abstract import AbstractRepository
from src.app.domain.submissions import SubmissionEntity


class SubmissionRepository(AbstractRepository[SubmissionEntity]):

    def add(self, submission_entity: SubmissionEntity) -> SubmissionEntity:
        self.session.add(submission_entity)
        self.session.flush()
        return submission_entity

    def get_by_member_id(self, member_id: str) -> List[SubmissionEntity]:
        return self.session.query(SubmissionEntity) \
            .filter(SubmissionEntity.member_id == member_id) \
            .all()
