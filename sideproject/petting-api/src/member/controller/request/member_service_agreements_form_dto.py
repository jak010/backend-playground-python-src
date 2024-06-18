from fastapi import Form
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, field_validator


class RequestMemberTemsrOfAgreementsFormDTO(BaseModel):
    """ Member, Service terms of  Agreement"""

    terms_of_age: bool
    terms_of_agreement: bool
    terms_of_privacy: bool
    terms_of_geolocation: bool
    terms_of_marketing: bool

    @classmethod
    def as_form(cls,
                terms_of_age: bool = Form(),
                terms_of_agreement: bool = Form(),
                terms_of_privacy: bool = Form(),
                terms_of_geolocation: bool = Form(),
                terms_of_marketing: bool = Form(default=False)
                ):
        return cls(
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
        return value

    @field_validator('terms_of_agreement')
    def allow_terms_of_agreement(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="`terms_of_agreement` field, must be true")
        return value

    @field_validator('terms_of_privacy')
    def allow_terms_of_privacy(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="`terms_of_privacy` field, must be true")
        return value

    @field_validator('terms_of_geolocation')
    def allow_terms_of_geolocation(cls, value):
        if not value:
            raise HTTPException(status_code=400, detail="`terms_of_geolocation` field, must be true")
        return value
