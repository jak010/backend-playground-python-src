import dataclasses

from sqlalchemy.orm import registry, relationship, foreign

from usages.database_usecase.config.sa_models import metadata, Member, MemberProfile

from usages.database_usecase.excercieses.imperative_mapping_style.entities import MemberEntity, MemberProfileEntity


def start_mapper(lazy_option=None):
    orm_mapper = registry(metadata)
    orm_mapper.map_imperatively(MemberProfileEntity, MemberProfile)
    orm_mapper.map_imperatively(
        MemberEntity, Member,
        properties={
            'profile': relationship(
                MemberProfileEntity,
                primaryjoin=(
                        Member.nanoid == foreign(MemberProfile.nanoid)
                ),
                lazy=lazy_option,
                uselist=True
            )
        }
    )

    return orm_mapper
