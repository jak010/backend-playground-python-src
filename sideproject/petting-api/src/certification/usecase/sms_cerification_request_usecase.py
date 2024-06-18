from __future__ import annotations

from libs.abstract.abstract_usecase import AbstractUseCase
from libs.utils.token_utils import SessionToken
from src.session.entity import SessionEntity
from src.certification.entity import (
    CeritifcationEntity,
    CerificationStatus,
    CerificationType
)
from src.certification.repository import CerificationRDBRepository
from src.member.repository import MemberRDBRepository
from settings.container.adapter_container import (
    AligoAdapterContainer,
    SMSApi
)
from dependency_injector.wiring import Provide


class AlredaySmsCerificationRequestException(Exception):
    """ Already Send, SMS Cerification Code """


class AlreadyCerificationCompleteException(Exception):
    """ Already Cerification Complete """


class SmsCerificationRequestUseCase(AbstractUseCase):
    member_repository = MemberRDBRepository()
    cerification_repository = CerificationRDBRepository()

    aligo_sms_api: SMSApi = Provide[AligoAdapterContainer.sms_api]

    def execute(self, session: SessionEntity):
        sms_cerification_complete = self.cerification_repository.find_sms_cerification_complete(
            member_id=session.member_id
        )
        if sms_cerification_complete:
            raise AlreadyCerificationCompleteException()

        sms_certification = self.cerification_repository.find_sms_cerification_in_request_with_member(
            member_id=session.member_id
        )

        if sms_certification:
            raise AlredaySmsCerificationRequestException()

        cerification_entity = CeritifcationEntity.new(
            member_id=session.member_id,
            phone=session.member.phone_number,
            code=self._sms_code(),
            status=CerificationStatus.REQUEST,
            type=CerificationType.SMS
        )

        self.aligo_sms_api.sms_send(
            receiver=session.member.phone_number,
            title="[FutureByte] 문자 인증",
            message=self._sms_code()
        )

        self.cerification_repository.add(cerification_entity)
        return cerification_entity

    def _sms_code(self):
        import random

        random_numbers = random.sample(range(10), 6)
        return ''.join(map(str, random_numbers))
