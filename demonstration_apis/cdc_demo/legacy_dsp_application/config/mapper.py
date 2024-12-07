from sqlalchemy.orm import registry

from . import orm

from src.domain.user.legacy_user import LegacyUser
from src.domain.campaign.legacy_campaign import LegacyCampaign
from src.domain.adgroup.legacy_adgroup import LegacyAdGroup
from src.domain.keyword.legacy_keyword import LegacyKeyword


def start_mapper():
    mapper = registry()
    mapper.map_imperatively(LegacyUser, orm.LegacyUser.__table__)
    mapper.map_imperatively(LegacyCampaign, orm.LegacyCampaign.__table__)
    mapper.map_imperatively(LegacyAdGroup, orm.LegacyAdgroup.__table__)
    mapper.map_imperatively(LegacyKeyword, orm.LegacyKeyword.__table__)
    return mapper
