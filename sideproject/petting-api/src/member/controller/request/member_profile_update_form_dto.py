from __future__ import annotations

from datetime import datetime, date
from typing import Literal, Optional

from fastapi import Form
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, field_validator

MBTI = Literal[
    'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
    'ISTP', 'ISFP', 'INFP', 'INTP',
    'ESTP', 'ESFP', 'ENFP', 'ENTP',
    'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
]
GENDER = Literal['MAIL', 'FEMAIL']


class MemberProfileUpdateFormDTO(BaseModel):
    nickname: Optional[str]
    description: Optional[str]
    address: Optional[str]
    job: Optional[str]
    birthday: Optional[datetime]
    gender: Optional[GENDER]

    @classmethod
    def as_form(cls,
                nickname: Optional[str] = Form(description="nick", default=None),
                description: Optional[str] = Form(description="description", default=None),
                address: Optional[str] = Form(description="address", default=None),
                job: Optional[str] = Form(description="job", default=None),
                birthday: Optional[date] = Form(description="BIRTDAY(EX. 2008-09-15)", default=None),
                gender: Optional[GENDER] = Form(description="GENDER", default=None),
                mbti: Optional[MBTI] = Form(description="MBTI", default=None),
                ):
        return cls(
            nickname=nickname,
            description=description,
            address=address,
            job=job,
            birthday=birthday,
            gender=gender,
            mbti=mbti
        )

    mbti: Optional[MBTI]

    @field_validator('nickname')
    def allow_nickname(cls, value: str):
        if value is None:
            return value

        if value.isalnum() and len(value) <= 6:
            return value
        raise HTTPException(status_code=400, detail="")

    @field_validator('birthday')
    def allow_birthday(cls, value: datetime) -> datetime:
        if value is None:
            return value

        try:
            return value
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid Format")
