import dataclasses
from typing import Optional

import nanoid


@dataclasses.dataclass
class MemberEntity:
    member_id: str
    name: str

    pk: Optional[int] = dataclasses.field(default=None)

    @classmethod
    def new(cls, name):
        return cls(
            member_id=nanoid.generate(size=24),
            name=name
        )
