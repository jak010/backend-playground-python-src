from __future__ import annotations

from libs.abstract.abstract_usecase import AbstractUseCase
from src.assessment.repository import AssessmentRDBRepository
from src.member.entity import MemberAssetEntity
from src.member.repository import MemberAssetRDBRepository


class AssessmentCompleteUseCase(AbstractUseCase):

    @classmethod
    def complete(cls, assessment_id: str, reason: str):
        """ 사용자 심사 완료 (STATUS : APPROVE) """

        _ISSUED_QUANTITY = 1  # 심사 완료시 발급 수량

        assessment = AssessmentRDBRepository.find_assessment_by_pk(nanoid=assessment_id)

        if assessment:
            assessment.update_approve(reason=reason)
            AssessmentRDBRepository.add(entity=assessment)

        MemberAssetRDBRepository.add(
            entity=MemberAssetEntity.new(
                issued_quantity=_ISSUED_QUANTITY,
                reason="ASSESSMENT APPROVE"
            ))
