from datetime import datetime

from .legacy_user import LegacyUser
from .i_legacy_user_repository import ILegacyUserRepository

from fastapi.exceptions import HTTPException


class LegacyUserService:
    repo = ILegacyUserRepository()

    def create(self, name: str) -> LegacyUser:
        """ 유저 생성하기 """
        return self.repo.save_user(
            LegacyUser.of(name=name)
        )

    def search_legacy_user_by_id(self, user_id: int) -> LegacyUser:
        """ 유저 조회하기 """
        user = self.repo.find_legacy_user_by_id(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="user not found")
        if user.deleted_at is not None:
            raise HTTPException(status_code=400, detail="this user is deleted")
        return user

    def delete_legacy_user_by_id(self, user_id: int) -> LegacyUser:
        """ 유저 삭제하기 (soft delete) """
        user = self.repo.find_legacy_user_by_id(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="user not found")
        user.deleted_at = datetime.now()
        return self.repo.save_user(user)

    def update_name(self, user_id, name: str):
        """ 유저 이름 업데이트 """
        user = self.repo.find_legacy_user_by_id(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="user not found")

        user.name = name
        return self.repo.save_user(user)
