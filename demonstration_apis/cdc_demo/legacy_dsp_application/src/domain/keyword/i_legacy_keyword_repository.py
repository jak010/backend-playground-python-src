from src.infrastructure.repositories.sqlalchemy_repository import ISqlalchemyRepositoryV2

from .legacy_keyword import LegacyKeyword


class ILegacyKeywordRepository(ISqlalchemyRepositoryV2[LegacyKeyword]): ...
