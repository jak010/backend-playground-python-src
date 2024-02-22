from sqlalchemy.orm import registry

from core.entity.member_entity import MemberEntity
from core.entity.member_profile_entity import MemberProfileEntity
from src import orm


def start_mapper():
    orm_mapper = registry()
    orm_mapper.map_imperatively(MemberEntity, orm.Member)
    orm_mapper.map_imperatively(MemberProfileEntity, orm.MemberProfile)
    return orm_mapper
