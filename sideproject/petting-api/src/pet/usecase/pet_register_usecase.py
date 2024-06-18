from __future__ import annotations

from libs.abstract.abstract_usecase import AbstractUseCase
from libs.utils.token_utils import SessionToken
from src.pet.controller.requests import PetRegisterRequestFormDTO
from src.pet.entity import PetEntity
from src.pet.repository import PetRDBRepository
from src.pet.repository.exception import PetEntityDuplicateException
from src.pet.enums import (
    PetPDTIType,
    PetPDTI,
    PetNeuteredStatus
)


class PetRegisteredLimitException(Exception):
    """ 등록 가능한 Pet 초과 """


class PetDuplicateException(Exception):
    """ Pet 중복됨 """


class PetRegisterUseCase(AbstractUseCase):
    MAX_REGISTERED_NUMBER = 10  # 등록 가능한 최대 Pet의 수

    pet_repository = PetRDBRepository()

    def execute(
            self,
            session: SessionToken,
            request: PetRegisterRequestFormDTO
    ) -> PetEntity:
        pets = self.pet_repository.find_pet_by_member(member_id=session.member_id)

        if len(pets) >= self.MAX_REGISTERED_NUMBER:
            raise PetRegisteredLimitException()

        try:
            saved_pet = self.pet_repository.add(
                pet_entity=PetEntity.new(
                    owner=session.member_id,
                    name=request.pet_name,
                    gender=request.pet_gender,
                    neutered_status=PetNeuteredStatus.to(value=request.pet_neutered_status),
                    breed=request.pet_breed,
                    pdti=PetPDTI.to(value=request.pet_pdti),
                    pdti_type=PetPDTIType.to(value=request.pet_pdti),
                ))
        except PetEntityDuplicateException:
            raise PetDuplicateException()
        return saved_pet
