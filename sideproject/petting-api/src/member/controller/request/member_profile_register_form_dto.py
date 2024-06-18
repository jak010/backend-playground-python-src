import datetime

from fastapi import Form
from pydantic import BaseModel


class MemberProfileRegisterFormDTO(BaseModel):
    nickname: str
    gender: str
    birthday: datetime.datetime
    mbti: str
    job: str

    @classmethod
    def as_form(cls,
                nickname: str = Form(title="nickname", description="사용자 닉네임"),
                gender: str = Form(title="gender", description="사용자 성별"),
                birthday: datetime.datetime = Form(title="birthday", description="사용자 생일"),
                mbti: str = Form(title="mbti", description="사용자 MBTI"),
                job: str = Form(title="job", description="사용자 직업"),
                description: str = Form(title="description", description="사용자 소개", default=None)
                ):
        return cls(
            nickname=nickname,
            gender=gender,
            birthday=birthday,
            mbti=mbti,
            job=job,
            description=description
        )
