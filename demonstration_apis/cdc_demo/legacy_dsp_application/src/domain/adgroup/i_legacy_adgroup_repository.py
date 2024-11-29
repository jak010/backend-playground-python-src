from typing import TypeVar

from src.infrastructure.repositories.sqlalchemy_repository import ISqlalchemyRepository as _ISqlalchemyRepository
from .legacy_adgroup import LegacyAdGroup

T = TypeVar("T", bound=LegacyAdGroup)


class ILegacyUserRepository(_ISqlalchemyRepository):

    def save_user(self, model: LegacyAdGroup) -> LegacyAdGroup:
        self.session.add(model)
        self.session.flush()
        self.session.refresh(model)
        self.session.commit()
        return model

    def find_legacy_adgroup_by_id(self, user_id: int) -> LegacyAdGroup:
        query = self.session.query(LegacyAdGroup).filter(LegacyAdGroup.id == user_id)
        if query.one_or_none():
            user = query.first()
            self.session.commit()
            return user
