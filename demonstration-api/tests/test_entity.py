from unittest import TestCase

from core.entity.member_entity import MemberEntity


class TestMemberEntity(TestCase):
    def test_member_entity(self):
        member1 = MemberEntity.new(name='kim', age=16)
        member2 = MemberEntity.new(name='park', age=16)

        assert member1 != member2

    def test_member_entity2(self):
        member1 = MemberEntity.new(name='kim', age=16)
        member2 = MemberEntity.new(name='park', age=16)

        assert member1.age == member2.age

    def test_member_entity3(self):
        member1 = MemberEntity.new(name='kim', age=16)
        member2 = MemberEntity.new(name='park', age=16)

        assert member1.name != member2.name
