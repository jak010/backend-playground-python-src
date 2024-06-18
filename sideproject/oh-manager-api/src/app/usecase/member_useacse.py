from src.app.domain import SessionEntity
from src.app.domain.aggregate.member_aggregate import MemeberAggregate
from src.app.usecase.abstract import AbstractUseCase
from src.app.usecase.exceptions.member import MemberCategoryDuplicate
from src.app.domain.member.command_query.member_category import MemberCategoryQuery, MemberCategoryCommand, \
    MemberCategoryDuplicateError


class MemberReadUseCase(AbstractUseCase):

    @classmethod
    def execute(cls, session: SessionEntity) -> MemeberAggregate:
        member_entity = cls.member_repository.get_by_id(member_id=session.member_id)

        member_aggregate = MemeberAggregate(root_entity=member_entity)

        return member_aggregate


class MemberCategoryUpdateUsecase(AbstractUseCase):

    @classmethod
    def execute(cls, session: SessionEntity, primary: str, secondary: str = None):
        # TODO, 2024.01.25 데이터 중복 Exception 처리하기
        try:
            MemberCategoryCommand.insert(
                member_id=session.member_id,
                primary=primary,
                secondary=secondary
            )
        except MemberCategoryDuplicateError:
            raise MemberCategoryDuplicate()


