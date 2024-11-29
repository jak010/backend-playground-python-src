from src.infrastructure.repositories.sqlalchemy_repository import ISqlalchemyRepositoryV2

from .legacy_campaign import LegacyCampaign


class ILegacyCampaignRepository(ISqlalchemyRepositoryV2[LegacyCampaign]): ...
