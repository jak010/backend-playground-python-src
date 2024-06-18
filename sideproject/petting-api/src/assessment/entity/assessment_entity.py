from __future__ import annotations

import datetime

from libs.abstract.abstract_entity import AbstractEntity
from src.assessment.value_object import AssessmentStatus


class AssessmentEntity(AbstractEntity):
    nanoid: str
    member_id: str
    status: str
    reason: str
    created_at: datetime.datetime
    modified_at: datetime.datetime

    @classmethod
    def new(cls,
            member_id: str,
            status: AssessmentStatus
            ) -> AssessmentEntity:
        return cls(
            nanoid=cls.generate_nano_id(),
            member_id=member_id,
            status=status,
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now()
        )

    def update_wait(self, reason: str):
        self.status = AssessmentStatus.WAIT.value
        self.reason = reason
        self.modified_at = datetime.datetime.now()

    def update_reject(self, reason: str):
        self.status = AssessmentStatus.REJECT.value
        self.reason = reason
        self.modified_at = datetime.datetime.now()

    def update_approve(self, reason: str):
        self.status = AssessmentStatus.APPROVE.value
        self.reason = reason
        self.modified_at = datetime.datetime.now()
