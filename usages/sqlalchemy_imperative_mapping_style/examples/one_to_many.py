from typing import List

from sqlalchemy.orm import registry, relationship, foreign

from usages.sqlalchemy_imperative_mapping_style import utils
from usages.sqlalchemy_imperative_mapping_style.examples import base_model
from usages.sqlalchemy_imperative_mapping_style.examples._entity import MemberProfileEntity


class MemberEntity:
    nanoid: str
    name: str
    age: int

    profile: List[MemberProfileEntity]


def start_mapper():
    orm_mapper = registry(base_model.metadata)

    orm_mapper.map_imperatively(MemberProfileEntity, base_model.MemberProfile)
    orm_mapper.map_imperatively(
        MemberEntity, base_model.Member,
        properties={
            'profile': relationship(
                MemberProfileEntity,
                primaryjoin=(
                        base_model.Member.nanoid == foreign(base_model.MemberProfile.nanoid)
                ),
                lazy='joined',
                uselist=True
            )
        }
    )

    return orm_mapper


class Repository:

    def __init__(self):
        self.session = utils.get_session()

    def find_by_member_id(self, member_id) -> MemberEntity:
        query = self.session.query(MemberEntity).filter(MemberEntity.nanoid == member_id).one_or_none()

        return query

    def update(self, member: MemberEntity):
        # One To May By OBJECT(MEMBER)
        self.session.add(member)
        for profile in member.profile:
            self.session.add(profile)
        self.session.commit()


if __name__ == '__main__':
    """ ONE TO MANY
    
    MEMBER (1..*) <---> (1) MEMBER_PROFILE

    """

    start_mapper()

    repository = Repository()
    member = repository.find_by_member_id(member_id='iy7nu9a0BEDBRe7LA1arjqjk')

    print("=" * 100)
    print(member)
    print(member.profile)
    print("=" * 100)

    # Update
    member.name = 'member_name_update1'
    member.age = 999
    member.profile[0].description = 'this is update test'
    member.profile[1].description = 'this is update test'

    # Insert ?
    # member = MemberEntity(
    #     nanoid=_nanoid.generate(size=24),
    #     name="this new member"
    # )
    # member.profile.append(MemberProfileEntity(
    #     nanoid=member.nanoid,
    #     description='this new description'
    # ))

    repository.update(member)
