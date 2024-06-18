from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PetDto(BaseModel):
    nanoid: Optional[str]

    name: Optional[str]
    gender: Optional[str]
    neutered_status: Optional[bool]
    breed: Optional[str]
    pdti: Optional[str]
    pdti_type: Optional[str]
    created_at: Optional[datetime]
