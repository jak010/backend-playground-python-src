from __future__ import annotations

from typing import Optional

from libs.abstract.abstract_rdb_repository import AbstracrtRDBRepository as _AbstracrtRDBRepository
from src.assessment.entity import AssessmentEntity


class AssessmentRDBRepository(_AbstracrtRDBRepository):

    @classmethod
    def add(cls, entity: AssessmentEntity) -> AssessmentEntity:
        cls.session.add(entity)
        return entity

    @classmethod
    def find_assessment_by_pk(cls, nanoid: str) -> Optional[AssessmentEntity]:
        query = cls.session.query(AssessmentEntity) \
            .filter(AssessmentEntity.nanoid == nanoid) \
            .one_or_none()
        if query:
            return query

    @classmethod
    def find_assessment_by_member_id(cls, member_id: str) -> Optional[AssessmentEntity]:
        query = cls.session.query(AssessmentEntity) \
            .filter(AssessmentEntity.member_id == member_id) \
            .one_or_none()
        if query:
            return query
