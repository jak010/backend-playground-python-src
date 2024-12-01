from sqlalchemy.orm import registry

from . import orm

from src.domain.legacy_user.legacy_user import LegacyUser
from src.domain.campaign.legacy_campaign import LegacyCampaign
from src.domain.adgroup.legacy_adgroup import LegacyAdGroup


def start_mapper():
    mapper = registry()
    mapper.map_imperatively(LegacyUser, orm.LegacyUser.__table__)
    mapper.map_imperatively(LegacyCampaign, orm.LegacyCampaign.__table__)
    mapper.map_imperatively(LegacyAdGroup, orm.LegacyAdgroup.__table__)
    return mapper
