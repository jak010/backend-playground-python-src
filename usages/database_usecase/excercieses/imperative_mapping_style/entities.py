import dataclasses


@dataclasses.dataclass
class MemberEntity:
    pk: int
    nanoid: str
    name: str
    age: int
    address1: str
    address2: str


@dataclasses.dataclass
class MemberProfileEntity:
    pk: int
    nanoid: int
    description: str
