from fastapi import Path, Body
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LegacyUserResponse(BaseModel):  # TODO, 241129 : Info 객체에 의한 Generic 으로 리팩터링 하면 깔끔할 듯
    id: Optional[int]
    name: str

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class LegacyUserCreateSchema:
    class LegacyUserCreateRequest(BaseModel):
        name: str

    class LegacyUserCreateResponse(LegacyUserResponse): ...


class LegacyUserRetreieveSchema:
    class LegacyUserFetchRequest(BaseModel):
        user_id: int = Path()

    class LegacyUserFetchResponse(LegacyUserResponse): ...


class LegacyUserUpdateSchema:
    class LegacyUserUpdateNameRequest(BaseModel):
        user_id: int
        name: str

        @classmethod
        def as_body(cls,
                    user_id=Path(),
                    name=Body(description="user name", embed=True)  # NOTE, 241130 : 단일값을 swagger에 요청받기
                    ):
            return cls(
                user_id=user_id,
                name=name
            )

    class LegacyUserUpdateNameResponse(LegacyUserResponse): ...


class LegacyUserDeleteSchema:
    class LegacyUserRemoveRequest(BaseModel):
        user_id: int = Path()
