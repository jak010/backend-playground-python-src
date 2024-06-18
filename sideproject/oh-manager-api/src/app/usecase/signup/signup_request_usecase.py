from src.app.domain.member import MemberEntity, MemberService, MemberActiveCode
from src.app.domain.verification import VerificationService
from src.app.usecase.abstract import AbstractUseCase
from src.app.usecase.exceptions.member import AlreadyExistEmail
from src.app.usecase.exceptions.validation import InvalidEmail


class SignUpRequestUsecase(AbstractUseCase):

    @classmethod
    def execute(
            cls,
            member_email: str,
            member_password: str
    ):
        if not MemberService.validate_email(member_email=member_email):
            raise InvalidEmail()

        member_entity = cls.member_repository.get_by_email(email=member_email)
        if member_entity:
            raise AlreadyExistEmail()

        member_entity = MemberEntity.new(
            email=member_email,
            password=MemberService.encryption_password(password=member_password),
            is_active=MemberActiveCode.DEACTIVE.value
        )
        verification_entity = VerificationService.send_email(
            member_entity=member_entity
        )

        cls.member_repository.add(member_entity)
        cls.verification_repository.add(verification_entity)
