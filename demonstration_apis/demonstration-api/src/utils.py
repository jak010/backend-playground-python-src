from sqlalchemy.orm import registry, relationship

from src.domain.entity import MemberEntity, MemberProfileEntity, MemberAggregate
from sqlalchemy.orm import joinedload, join, outerjoin, composite
from src import orm
from sqlalchemy.orm import deferred, lazyload, joinedload, backref, join, aliased, composite, mapper, Mapper, selectinload
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy import alias
from src.domain.value_object.address import Address
from sqlalchemy.orm import Bundle

from src.domain.entity.member_aggregate import MemberAggregate


def start_mapper():
    orm_mapper = registry(orm.metadata)
    orm_mapper.map_imperatively(MemberProfileEntity, orm.MemberProfile)

    orm_mapper.map_imperatively(MemberEntity, orm.Member)

    print('*' * 10)
    print(dir(orm.Member.__table__.c.keys()))
    print(orm.Member.__table__.c.keys())
    # print(orm.Member.__table__.c._all_columns)

    print('*' * 10)

    orm_mapper.map_imperatively(
        MemberAggregate, orm.Member,

        properties={
            'root_entity_id': orm.Member.__table__.c.nanoid,

            'profile': relationship(
                MemberProfileEntity,
                backref='member',
                lazy='joined',
                primaryjoin='member.c.nanoid == foreign(member_profile.c.nanoid)',
                uselist=True,

            )
        }
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
