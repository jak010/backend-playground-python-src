from typing import List, Dict

from src.app.domain import SubmissionEntity
from src.app.domain.aggregate.submission_aggregate import SubmissionAggregate
from src.app.domain.session.session_entity import SessionEntity
from src.app.usecase.abstract import AbstractUseCase
from src.app.usecase.exceptions.validation import InvalidSubmissions, InvalidAuditions


class ReadSubmissionListUseCase(AbstractUseCase):
    @classmethod
    def execute(cls, session: SessionEntity) -> List[Dict]:
        aggregates = []
        for submission in cls.submission_repository.get_by_member_id(member_id=session.member_id):
            aggregates.append(
                SubmissionAggregate(root_entity=submission)
            )

        return [aggregate.read() for aggregate in aggregates]


class SubmissionsApplyUseCase(AbstractUseCase):

    @classmethod
    def execute(cls, session: SessionEntity, audition_id: int):
        audition = cls.auditions_repository.get_by_id(audition_id=audition_id)
        if audition is None:
            raise InvalidAuditions()

        try:
            cls.submission_repository.add(
                submission_entity=SubmissionEntity.new(
                    audition_id=audition.id,
                    member_id=session.member_id,
                    status=""  # TODO, 24.01.29 : SUBMISSIONS STATUS 설정 필요
                ))
        except Exception:
            raise InvalidSubmissions()
