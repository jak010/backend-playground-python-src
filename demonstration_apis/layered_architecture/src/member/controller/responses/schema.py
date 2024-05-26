from pydantic import BaseModel


class MemberResponseModel(BaseModel):
    pk: int
    name: str
    age: int
