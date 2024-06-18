from dependency_injector import providers, containers

from src.app.domain import (
    MemberRepository,
    VerificationRepository,
    SessionRepository,
    ProfileRepository,
    AuditionRepository,
    SubmissionRepository
)


class RepositoryContainer(containers.DeclarativeContainer):
    member_repository = providers.Singleton(MemberRepository)
    verification_repository = providers.Singleton(VerificationRepository)

    session_repository = providers.Singleton(SessionRepository)
    profile_repository = providers.Singleton(ProfileRepository)
    auditions_repository = providers.Singleton(AuditionRepository)
    submission_repository = providers.Singleton(SubmissionRepository)
