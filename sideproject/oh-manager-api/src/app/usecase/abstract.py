from abc import ABCMeta

from dependency_injector.wiring import Provide

from src.app.domain import (
    MemberRepository,
    VerificationRepository,
    SessionRepository,
    ProfileRepository,
    AuditionRepository,
    SubmissionRepository
)
from src.config.container.repository_container import RepositoryContainer


class AbstractUseCase(metaclass=ABCMeta):
    member_repository: MemberRepository = Provide[RepositoryContainer.member_repository]
    session_repository: SessionRepository = Provide[RepositoryContainer.session_repository]
    verification_repository: VerificationRepository = Provide[RepositoryContainer.verification_repository]

    profile_repository: ProfileRepository = Provide[RepositoryContainer.profile_repository]
    auditions_repository: AuditionRepository = Provide[RepositoryContainer.auditions_repository]
    submission_repository: SubmissionRepository = Provide[RepositoryContainer.submission_repository]

    @classmethod
    def execute(cls, *args, **kwargs): ...
