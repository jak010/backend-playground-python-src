from .legacy_user import LegacyUser
from .i_legacy_user_repository import ILegacyUserRepository


class LegacyUserService:
    repo = ILegacyUserRepository()

    def create(self, name: str):
        new_user = LegacyUser.of(name=name)
        self.repo.save_user(model=new_user)
        return new_user
