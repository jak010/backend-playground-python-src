import random
import uuid

from sqlalchemy.orm import registry, relationship

from src.domain.member.entity import MemberEntity, MemberProfileEntity, MemberAggregate
from src.domain.posts.post_entity import PostEntity
from sqlalchemy.orm import joinedload, join, outerjoin, composite
from src import orm
from sqlalchemy.orm import deferred, lazyload, joinedload, backref, join, aliased, composite, mapper, Mapper, selectinload
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy import alias
from src.domain.member.value_object.address import Address
from sqlalchemy.orm import Bundle
from sqlalchemy.orm.attributes import set_committed_value
from settings.dev import get_engine


# version controal : https://stackoverflow.com/questions/60799213/sqlalchemy-version-id-col-and-version-id-generator-not-working-with-classical-ma

def start_mapper():
    orm_mapper = registry(orm.metadata)
    orm_mapper.map_imperatively(MemberProfileEntity, orm.MemberProfile)

    orm_mapper.map_imperatively(MemberEntity, orm.Member)
    orm_mapper.map_imperatively(
        PostEntity,
        orm.Post,
        version_id_col=orm.Post.__table__.c.version,
    )

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
