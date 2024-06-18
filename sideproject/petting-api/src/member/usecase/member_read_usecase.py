from typing import Tuple, List, Optional, Dict

from src.member.entity import MemberEntity, MemberProfileEntity
from src.pet.controller.dto import PetDto, PetAttachmentDto
from src.session.entity import SessionEntity
from .abstract_member_usecase import AbstractMemberUseCase


class MemberReadUseCase(AbstractMemberUseCase):

    def execute(self, session: SessionEntity) -> Dict:
        member = self.member_rdb_repository.find_member_by_nanoid(nanoid=session.member_id)
        member_profile = self.member_profile_rdb_repository.find_member_profile_by_nanoid(nanoid=member.nanoid)
        pet = self.pet_rdb_repository.find_pet_primary(member_id=member.nanoid)

        data = {
            "member": member,
            "member_profile": member_profile,
            "pet": None,
            "pet_attachment": None
        }
        #
        if pet:
            data["pet"] = PetDto(
                nanoid=pet.nanoid,
                name=pet.name,
                neutered_status=pet.neutered_status,
                gender=pet.gender,
                breed=pet.breed,
                pdti=pet.pdti,
                pdti_type=pet.pdti_type,
                created_at=pet.created_at
            )
            pet_attatchment = self.pet_attachment_rdb_repository.find_pet_attachment_by_primary(
                member_id=member.nanoid, pet_nano_id=pet.nanoid
            )
            if pet_attatchment:
                data["pet_attachment"] = PetAttachmentDto(
                    attachment_type=pet_attatchment.attachment_type,
                    attachment_label=pet_attatchment.attachment_label,
                    s3_key=pet_attatchment.s3_key,
                    content_type=pet_attatchment.content_type,
                    created_at=pet_attatchment.created_at
                )

        return data
