from typing import List

from src.app.domain import AuditionEntity
from src.app.domain.session.session_entity import SessionEntity
from src.app.usecase.abstract import AbstractUseCase


class ReadAuditionListUseCase(AbstractUseCase):

    @classmethod
    def execute(cls, session: SessionEntity, page: int, item_per_page: int) -> List[AuditionEntity]:
        member = cls.member_repository.get_by_id(member_id=session.member_id)
        submissions = cls.submission_repository.get_by_member_id(member_id=member.id)
        member_categories = [member_category.primary for member_category in member.category]

        if member_categories:
            submission_ids = [int(submission.audition_id) for submission in submissions]

            auditions = cls.auditions_repository.get_by_categories(
                categories=member_categories,
                page=page,
                submissions=submission_ids,
                item_per_page=item_per_page
            )
            return auditions
