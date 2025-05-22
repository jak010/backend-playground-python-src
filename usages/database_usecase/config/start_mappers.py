from sqlalchemy.orm import registry

from sqlalchemy.orm import registry

from usages.sqlalchemy_imperative_mapping_style.config.sa_models import metadata


def start_mapper():
    orm_mapper = registry(metadata)

    # orm_mapper.map_imperatively(MemberProfileEntity, base_model.MemberProfile)
    # orm_mapper.map_imperatively(
    #     MemberEntity, base_model.Member,
    #     properties={
    #         'profile': relationship(
    #             MemberProfileEntity,
    #             primaryjoin=(
    #                     base_model.Member.nanoid == foreign(base_model.MemberProfile.nanoid)
    #             ),
    #             lazy='joined',
    #             uselist=True
    #         )
    #     }
    # )

    return orm_mapper
