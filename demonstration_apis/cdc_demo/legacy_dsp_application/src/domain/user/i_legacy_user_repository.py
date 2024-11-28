from typing import TypeVar

from src.infrastructure.repositories.sqlalchemy_repository import ISqlalchemyRepository as _ISqlalchemyRepository
from .legacy_user import LegacyUser

T = TypeVar("T", bound=LegacyUser)


class ILegacyUserRepository(_ISqlalchemyRepository):

    def save_user(self, model: LegacyUser):
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model
