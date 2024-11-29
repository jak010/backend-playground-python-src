from typing import TypeVar

from src.infrastructure.repositories.sqlalchemy_repository import ISqlalchemyRepository as _ISqlalchemyRepository
from .legacy_user import LegacyUser

T = TypeVar("T", bound=LegacyUser)


class ILegacyUserRepository(_ISqlalchemyRepository):

    def save_user(self, model: LegacyUser) -> LegacyUser:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def find_legacy_user_by_id(self, user_id: int) -> LegacyUser:
        query = self.session.query(LegacyUser).filter(LegacyUser.id == user_id)
        self.session.commit()
        return query.first()

    def delete_by_id(self, user_id: int):
        query = self.session.query(LegacyUser).filter(LegacyUser.id == user_id)
        query.delete()
        self.session.commit()
