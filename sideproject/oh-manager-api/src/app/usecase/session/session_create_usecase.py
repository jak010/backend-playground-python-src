from src.app.domain.member import MemberService, MemberActiveCode
from src.app.domain.session import SessionService
from src.app.usecase.abstract import AbstractUseCase
from src.app.usecase.exceptions.member import DoesNotExistMember, DeactivateMember
from src.app.usecase.exceptions.validation import InvalidCredential
from src.libs import token_util


class SessionCreateUseCase(AbstractUseCase):

    @classmethod
    def execute(cls, email: str, password: str) -> str:
        # TODO, 24.01.19: Exception 처리 필요함
        member_entity = cls.member_repository.get_by_email(email=email)
        if member_entity is None:
            raise DoesNotExistMember()
        if not MemberService.check_password(password=password, hased_password=member_entity.password):
            raise InvalidCredential()

        if member_entity.is_active == MemberActiveCode.DEACTIVE.value:
            raise DeactivateMember()

        session_entity = SessionService.create_session_for_one_hour(member_id=member_entity.id)
        cls.session_repository.add(session_entity)

        return token_util.create_access_token(
            session_id=session_entity.session_id,
            member_id=session_entity.member_id,
            iat=session_entity.iat,
            exp=session_entity.exp
        )
