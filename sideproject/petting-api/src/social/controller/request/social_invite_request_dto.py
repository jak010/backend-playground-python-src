from fastapi import Form, HTTPException
from pydantic import BaseModel, field_validator


class SocialInviteRequestDto(BaseModel):
    receiver_member: str

    @classmethod
    def as_form(
            cls,
            receiver_member: str = Form(description="chat receiver, member-id"),
    ):
        return cls(
            receiver_member=receiver_member
        )

    @field_validator("receiver_member")
    def allow_receiver_name(cls, value: str):
        if not value:
            raise HTTPException(status_code=400, detail="Bad Request, receiver_name")
        return value
