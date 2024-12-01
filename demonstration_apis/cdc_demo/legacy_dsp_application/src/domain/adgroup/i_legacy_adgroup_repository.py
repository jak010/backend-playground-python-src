from typing import TypeVar

from src.infrastructure.repositories.sqlalchemy_repository import ISqlalchemyRepositoryV2
from .legacy_adgroup import LegacyAdGroup

T = TypeVar("T", bound=LegacyAdGroup)


class ILegacyAdGroupRepository(ISqlalchemyRepositoryV2[LegacyAdGroup]):
    pass
