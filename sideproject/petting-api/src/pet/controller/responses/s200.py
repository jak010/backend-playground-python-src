from pydantic import BaseModel


class PetDto(BaseModel):
    nano_id: str
    name: str
