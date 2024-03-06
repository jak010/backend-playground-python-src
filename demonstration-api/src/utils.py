from sqlalchemy.orm import registry, relationship

from src.domain.entity import MemberEntity, MemberProfileEntity, MemberAggregate
from sqlalchemy.orm import joinedload, join, outerjoin, composite
from src import orm
from sqlalchemy.orm import deferred, lazyload, joinedload, backref, join, aliased, composite, mapper, Mapper
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy import alias
from src.domain.value_object.address import Address
from sqlalchemy.orm import Bundle


def start_mapper():
    orm_mapper = registry(orm.metadata)
    # orm_mapper.map_imperatively(MemberProfileEntity, orm.MemberProfile)

    orm_mapper.map_imperatively(
        MemberEntity, orm.Member,
        properties={
            "address": composite(
                Address,
                orm.Member.address1,
                orm.Member.address2,
            )
        },
        # Fix
        exclude_properties={
            orm.Member.address1,
            orm.Member.address2,
        },

    )

    return orm_mapper

    # orm_mapper.map_imperatively(MemberEntity, orm.Member,
    #     properties={
    #         # "exclude_columns": [
    #         #     orm.t_member.c.address1,
    #         #     orm.t_member.c.address2
    #         # ],
    #         'address': composite(
    #             Address,
    #             orm.Member.__table__.c.address1,
    #             orm.Member.__table__.c.address2
    #         ),
    #         # 'member_profile': relationship(
    #         #     orm.t_member_profile,
    #         #     primaryjoin='foreign(member.c.nanoid) == member_profile.c.nanoid',
    #             # lazy='joined',
    #             # uselist=False
    #         # )
    #     }

    # return orm_mapper


from sqlalchemy.orm import mapper
