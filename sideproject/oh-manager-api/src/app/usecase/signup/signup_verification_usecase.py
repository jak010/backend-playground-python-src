import time
import uuid

from src.app.domain.member import MemberActiveCode
from src.app.domain.profile import ProfileEntity
from src.app.domain.verification import VerificationStatus
from src.app.usecase.abstract import AbstractUseCase
from src.app.usecase.exceptions.verification import (
    VerificationCodeExpired,
    VerificationCodeIsNotPending,
    DoesNotExistVerification
)
from src.app.usecase.exceptions.member import AlreadyExistEmail, AlreadyJoinedMember
from src.libs.storage.member_storage import MemberStorage


class SignUpVerificationUsecase(AbstractUseCase):

    @classmethod
    def execute(
            cls,
            verification_code: str
    ):
        verification_entity = cls.verification_repository.get_pending_email_verification_by_code(
            code=verification_code
        )
        if verification_entity is None:
            raise DoesNotExistVerification()

        if verification_entity.expired_at < int(time.time()):
            cls.verification_repository.expired(verification_entity)
            raise VerificationCodeExpired()

        if verification_entity.status != VerificationStatus.PENDING.value:
            raise VerificationCodeIsNotPending()

        member_entity = cls.member_repository.get_by_email(email=verification_entity.receiver)
        if member_entity and (member_entity.is_active == MemberActiveCode.ACTIVE.value):
            raise AlreadyJoinedMember()

        member_entity.joined_at = int(time.time())
        member_entity.is_active = MemberActiveCode.ACTIVE.value

        profile_entity = ProfileEntity.new(
            member_id=member_entity.id,
            name=str(uuid.uuid4())[0:5]
        )

        MemberStorage.create_member_storage(member_id=member_entity.id)

        cls.verification_repository.approved(verification_entity)
        cls.profile_repository.add(profile_entity)
        return member_entity
