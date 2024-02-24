from notepad.structure.domain.i_xxx_repository import IXXXRepository
from notepad.structure.infra.SQLAlchemyMemberRepository import SQLAlchemyMemberRepository


class MemberEntity:
    name = None

    def change(self, name):
        """ Member Name Change Method """
        self.name = name


class Transactional:
    ...


class MemberService:

    @Transactional
    def change_xxx_info(self):
        member = SQLAlchemyMemberRepository.find_by_id(member_id=None)
        member.change(name='asdas')
