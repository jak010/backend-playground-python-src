import datetime
from functools import cached_property

from dependency_injector.wiring import Provide

from src.app.domain import (
    MemberRepository,
    SubmissionRepository, AuditionRepository, AuditionEntity
)
from src.app.domain.member.member_entity import MemberEntity
from src.app.domain.submissions import SubmissionEntity
from src.config.container.repository_container import RepositoryContainer


class SubmissionAggregate:
    member_repository: MemberRepository = Provide[RepositoryContainer.member_repository]
    submission_repository: SubmissionRepository = Provide[RepositoryContainer.submission_repository]
    auditions_repository: AuditionRepository = Provide[RepositoryContainer.auditions_repository]

    def __init__(self, root_entity: SubmissionEntity = None):
        self.root_entity = root_entity

    @cached_property
    def auditions(self) -> AuditionEntity:
        try:
            return self.auditions_repository.get_by_id(audition_id=self.root_entity.audition_id)
        except AttributeError:
            return None

    @cached_property
    def member(self) -> MemberEntity:
        try:
            return self.member_repository.get_by_id(member_id=self.root_entity.member_id)
        except AttributeError:
            return None

    def read(self):
        return {
            "submission": {
                "status": self.root_entity.status if self.root_entity is not None else str,
                "created_at": self.root_entity.created_at if self.root_entity is not None else datetime.datetime
            },
            "auditions": {
                "title": self.auditions.title if self.auditions is not None else str,
                "content": self.auditions.content if self.auditions is not None else str,
                "category": self.auditions.category if self.auditions is not None else str,
                "reward": self.auditions.reward if self.auditions is not None else str,
                "end_date": self.auditions.end_date.isoformat() if self.auditions is not None else str
            }
        }
