from fastapi import Form
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from .define import MemberChannel


class MemberRegisterFormDTO(BaseModel):
    """ 사용자 등록 """
    email: EmailStr
    name: str
    phone: str
    channel: MemberChannel
    terms_of_age: bool
    terms_of_agreement: bool
    terms_of_privacy: bool
    terms_of_geolocation: bool
    terms_of_marketing: bool

    @classmethod
    def as_form(cls,
                email: EmailStr = Form(title="email", description="사용자 이메일"),
                name: str = Form(title="name", description="사용자 이름"),
                phone: str = Form(title="phone", description="사용자 핸드폰"),
                channel: MemberChannel = Form(title="channel", description="가입채널"),
                terms_of_age: bool = Form(title='terms_of_age'),
                terms_of_agreement: bool = Form(title='terms_of_agreement'),
                terms_of_privacy: bool = Form(title='terms_of_privacy'),
                terms_of_geolocation: bool = Form(title='terms_of_geolocation'),
                terms_of_marketing: bool = Form(title='terms_of_marketing', default=False)
                ):
        return cls(
            email=email,
            name=name,
            phone=phone,
            channel=channel,
            terms_of_age=terms_of_age,
            terms_of_agreement=terms_of_agreement,
            terms_of_privacy=terms_of_privacy,
            terms_of_geolocation=terms_of_geolocation,
            terms_of_marketing=terms_of_marketing
        )

    @field_validator('terms_of_age')
    def allow_terms_of_age(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="`terms_of_age` field, must be true")

    @field_validator('terms_of_agreement')
    def allow_terms_of_agreement(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="`terms_of_agreement` field, must be true")

    @field_validator('terms_of_privacy')
    def allow_terms_of_privacy(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="`terms_of_privacy` field, must be true")

    @field_validator('terms_of_geolocation')
    def allow_terms_of_geolocation(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="`terms_of_geolocation` field, must be true")
