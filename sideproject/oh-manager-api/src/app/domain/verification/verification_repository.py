import time
from typing import Optional, NoReturn

from src.app.domain.abstract import AbstractRepository
from src.app.domain.verification import VerificationEntity, VerificationStatus, VerificationType


class VerificationRepository(AbstractRepository[VerificationEntity]):

    def add(self, verification_entity: VerificationEntity) -> VerificationEntity:
        self.session.add(verification_entity)
        return verification_entity

    def get_pending_email_verification_by_code(self, code: str) -> Optional[VerificationEntity]:
        query = self.session.query(VerificationEntity) \
            .filter(VerificationEntity.code == code) \
            .filter(VerificationEntity.type == VerificationType.EMAIL.value) \
            .filter(VerificationEntity.status == VerificationStatus.PENDING.value) \
            .order_by(VerificationEntity.created_at.desc()) \
            .first()
        if query:
            return query

    def expired(self, verification_entity: VerificationEntity) -> NoReturn:
        query = self.session.query(VerificationEntity) \
            .filter(VerificationEntity.code == verification_entity.code) \
            .filter(VerificationEntity.type == verification_entity.type) \
            .filter(VerificationEntity.status == verification_entity.status)
        query.update({
            "status": VerificationStatus.EXPIRED.value,
            "modified_at": int(time.time())
        })

    def approved(self, verification_entity: VerificationEntity) -> NoReturn:
        query = self.session.query(VerificationEntity) \
            .filter(VerificationEntity.code == verification_entity.code) \
            .filter(VerificationEntity.type == verification_entity.type) \
            .filter(VerificationEntity.status == verification_entity.status)
        query.update({
            "status": VerificationStatus.APPROVED.value,
            "modified_at": int(time.time())
        })
