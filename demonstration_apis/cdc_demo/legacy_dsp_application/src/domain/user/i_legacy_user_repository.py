from typing import TypeVar

from src.infrastructure.repositories.sqlalchemy_repository import ISqlalchemyRepository as _ISqlalchemyRepository
from .legacy_user import LegacyUser

T = TypeVar("T", bound=LegacyUser)


class ILegacyUserRepository(_ISqlalchemyRepository):

    def save_user(self, model: LegacyUser) -> LegacyUser:
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        self.session.commit()
        return model

    def find_legacy_user_by_id(self, user_id: int) -> LegacyUser:
        query = self.session.query(LegacyUser).filter(LegacyUser.id == user_id)
        if query.one_or_none():
            user = query.first()
            self.session.commit()
            return user
