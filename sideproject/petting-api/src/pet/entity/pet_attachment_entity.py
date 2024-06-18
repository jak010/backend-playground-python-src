from __future__ import annotations

import datetime
from typing import Optional

from libs.abstract.abstract_entity import AbstractEntity
from src.pet.enums import PetAttachmentType, PetAttachmentLabel


class PetAttachmentEntity(AbstractEntity):
    pk: int
    nanoid: str  # ref, pet.nanoid

    member_id: str
    attachment_type: str
    attachment_label: str

    s3_key: str
    file_name: str
    file_size: str
    content_type: str

    created_at: datetime.datetime
    modified_at: datetime.datetime

    @classmethod
    def new(cls,
            nanoid: str,
            member_id: str,
            attachment_type: PetAttachmentType,
            attachment_label: PetAttachmentLabel,
            s3_key: Optional[str],
            file_name: str,
            file_size: int,
            content_type: str
            ) -> PetAttachmentEntity:
        return cls(
            nanoid=nanoid,
            member_id=member_id,
            attachment_type=attachment_type.value,
            attachment_label=attachment_label.value,
            s3_key=s3_key,
            file_name=file_name,
            file_size=file_size,
            content_type=content_type,
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now()
        )
