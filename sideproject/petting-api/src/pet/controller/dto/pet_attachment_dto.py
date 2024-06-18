import datetime

from pydantic import BaseModel
from typing import Optional


class PetAttachmentDto(BaseModel):


    attachment_type: Optional[str]
    attachment_label: Optional[str]
    s3_key: Optional[str]
    content_type: Optional[str]
    created_at: Optional[datetime.datetime]
