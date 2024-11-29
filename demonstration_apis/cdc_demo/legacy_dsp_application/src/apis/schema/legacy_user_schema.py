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
        user_id: int = Path()
        name: str = Body()

    class LegacyUserUpdateNameResponse(LegacyUserResponse): ...


class LegacyUserDeleteSchema:
    class LegacyUserRemoveRequest(BaseModel):
        user_id: int = Path()
