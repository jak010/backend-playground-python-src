import datetime

from pydantic import BaseModel
from typing import Optional, List


class SocialInviteDto(BaseModel):
    social_id: int
    member_id: str
    pet_name: Optional[str]
    pet_breed: Optional[str]
    pet_pdit: Optional[str]
    pet_image: Optional[str]
    invited_time: str


class SocialInviteList(BaseModel):
    count: int
    items: List[SocialInviteDto]
