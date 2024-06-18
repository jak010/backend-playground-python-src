import random

from src.app.domain.member.member_entity import MemberEntity
from src.app.domain.verification.verification_entity import (
    VerificationEntity,
    VerificationStatus,
    VerificationType
)


class VerificationService:

    @classmethod
    def send_email(cls, member_entity: MemberEntity) -> VerificationEntity:
        entity = VerificationEntity.new(
            sender="test",
            receiver=member_entity.email,
            type=VerificationType.EMAIL.value,
            status=VerificationStatus.PENDING.value,
            code=cls().generate_code()
        )

        # TODO: 24.01.19: Email 전송 코드 구현 필요함

        return entity

    @staticmethod
    def generate_code():
        digits = random.choices(range(0, 10), k=6)
        return ''.join(str(x) for x in digits)
