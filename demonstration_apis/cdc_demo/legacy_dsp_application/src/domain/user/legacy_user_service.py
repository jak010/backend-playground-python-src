from .legacy_user import LegacyUser
from .i_legacy_user_repository import ILegacyUserRepository


class LegacyUserService:
    repo = ILegacyUserRepository()

    def create(self, name: str) -> LegacyUser:
        """ 유저 생성하기 """
        return self.repo.save_user(
            LegacyUser.of(name=name)
        )

    def search_legacy_user_by_id(self, user_id: int) -> LegacyUser:
        """ 유저 조회하기 """
        return self.repo.find_legacy_user_by_id(user_id=user_id)

    def delete_legacy_user_by_id(self, user_id: int) -> LegacyUser:
        """ 유저 조회하기 """
        return self.repo.delete_by_id(user_id=user_id)
