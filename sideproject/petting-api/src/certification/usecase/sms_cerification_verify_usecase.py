from __future__ import annotations

from libs.abstract.abstract_usecase import AbstractUseCase
from libs.utils.token_utils import SessionToken
from src.certification.repository import CerificationRDBRepository
from src.member.repository import MemberRDBRepository


class CertificationDoesNotExist(Exception):
    """ Certification Hisstory DoesNotExist """


class SmsCerificationVerifyUseCase(AbstractUseCase):
    member_repository = MemberRDBRepository()
    cerification_repository = CerificationRDBRepository()

    def execute(self, session: SessionToken, sms_code: str):
        sms_certification = self.cerification_repository.find_sms_certification_code_with_member(
            member_id=session.member_id,
            code=sms_code
        )
        if not sms_certification:
            raise CertificationDoesNotExist()

        self.cerification_repository.update_complete_sms_certification(
            member_id=session.member_id,
            code=sms_code
        )

        self.member_repository.update_member_cerification_phone(nanoid=session.member_id)
