from pydantic import BaseModel
from fastapi import Form


class AssessmentRequestFormDto(BaseModel):
    reason: str

    @classmethod
    def as_form(
            cls,
            reason: str = Form(description="이유")
    ):
        return cls(
            reason=reason
        )
