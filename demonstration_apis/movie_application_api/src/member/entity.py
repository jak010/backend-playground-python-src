from src.libs import utils
from src.libs.i_entity import AbstractEntity


class MemberEntity(AbstractEntity):
    member_id: str
    name: str

    @classmethod
    def new(cls, name):
        return cls(member_id=utils.generate_entity_id(), name=name)
