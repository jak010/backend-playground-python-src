from dependency_injector.wiring import Provide
from functools import cached_property
from src.app.domain import (
    MemberRepository,
    ProfileRepository
)
from src.app.domain.member.member_entity import MemberEntity
from src.app.domain.profile.profile_entity import ProfileEntity
from src.config.container.repository_container import RepositoryContainer


class MemeberAggregate:
    member_repository: MemberRepository = Provide[RepositoryContainer.member_repository]
    profile_repository: ProfileRepository = Provide[RepositoryContainer.profile_repository]

    def __init__(self, root_entity: MemberEntity):
        self.root_entity = root_entity

    def category(self):
        return self.root_entity.category

    @cached_property
    def profile(self) -> ProfileEntity:
        return self.profile_repository.get_by_member_id(member_id=self.root_entity.id)

    def read(self):
        return {
            "member": self.root_entity.read(
                exclude_fields=['password']
            ),
            "profile": self.profile.read(
                exclude_fields=['id', 'member_id']
            ),
            "category": [{
                "primary": category.primary,
                "secondary": category.secondary,
                "created_at": category.created_at
            } for category in self.category()]
        }
