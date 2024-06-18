from __future__ import annotations

from libs.abstract.abstract_usecase import AbstractUseCase
from settings.policy.define import PET_IMAGE_PRIMARY_LIMIT, PET_SELFIE_IMAGE_PRIMARY_LIMIT
from src.assessment.entity import AssessmentEntity
from src.assessment.repository import AssessmentRDBRepository
from src.assessment.value_object import AssessmentStatus

from src.pet.repository import PetAttachmentRDBRepository
from src.pet.enums import PetAttachmentLabel


class AssessmentRegisterUseCase(AbstractUseCase):
    pet_attachment_repository = PetAttachmentRDBRepository()

    @classmethod
    def execute(cls, member_id: str):
        """ 사용자 심사 등록 (STATUS : WAIT) """
        primary_counts = cls.pet_attachment_repository.find_by_pet_attachment_primary_aggregate()

        if cls.check_primary_image_limits(primary_counts):
            assessment = AssessmentRDBRepository.find_assessment_by_member_id(member_id=member_id)

            if assessment is None:
                AssessmentRDBRepository.add(
                    entity=AssessmentEntity.new(
                        member_id=member_id,
                        status=AssessmentStatus.WAIT.value
                    ))

    @classmethod
    def check_primary_image_limits(cls, primary_counts):
        """ PET & SELFIE는 각각 2개 이상의 대표(Primary) 사진 개수 체크  """
        return primary_counts[PetAttachmentLabel.PET.value] >= PET_IMAGE_PRIMARY_LIMIT and \
            primary_counts[PetAttachmentLabel.SELFIE.value] >= PET_SELFIE_IMAGE_PRIMARY_LIMIT
