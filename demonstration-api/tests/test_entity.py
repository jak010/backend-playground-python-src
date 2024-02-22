from unittest import TestCase

from core.entity import MemberEntity


class TestMemberEntity(TestCase):
    def test_member_entity(self):

        member1 = MemberEntity.new(name='hello', age='10')
