from __future__ import annotations

from libs.abstract.abstract_usecase import AbstractUseCase
from src.assessment.repository import AssessmentRDBRepository
from src.pet.repository import PetAttachmentRDBRepository


class AssessmentDeninedUseCase(AbstractUseCase):
    pet_attachment_repository = PetAttachmentRDBRepository()

    @classmethod
    def execute(cls, assessment_id: str, reason: str):
        """ 사용자 심사 거절 (STATUS : REJECT) """
        assessment = AssessmentRDBRepository.find_assessment_by_pk(nanoid=assessment_id)
        if assessment:
            assessment.update_reject(reason=reason)
            AssessmentRDBRepository.add(assessment)
