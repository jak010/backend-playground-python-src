from sqlalchemy.orm import registry

from . import orm

from src.domain.user.legacy_user import LegacyUser


def start_mapper():
    mapper = registry()
    mapper.map_imperatively(LegacyUser, orm.LegacyUser.__table__)
    return mapper
