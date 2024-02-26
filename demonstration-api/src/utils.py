from sqlalchemy.orm import registry, relationship

from core.domain.entity import MemberEntity, MemberProfileEntity, MemberAggregate
from sqlalchemy.orm import joinedload, join, outerjoin, composite
from src import orm
from sqlalchemy.orm import deferred, lazyload, joinedload, backref, join, aliased
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy import alias


def start_mapper():
    orm_mapper = registry(orm.metadata)
    orm_mapper.map_imperatively(MemberProfileEntity, orm.MemberProfile)

    orm_mapper.map_imperatively(
        MemberEntity, orm.Member,
        properties={
            'member_profile': relationship(
                MemberProfileEntity,
                backref=backref('member'),
                primaryjoin='foreign(member.c.nanoid) == member_profile.c.nanoid',
                # lazy='joined',
                # uselist=False
            )
        }
    )

    return orm_mapper
