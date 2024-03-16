import dataclasses

from src.domain.abstract import AbstractValueObject


@dataclasses.dataclass(frozen=True, eq=True)
class Address(AbstractValueObject):
    address1: str
    address2: str

    def __composite_values__(self):
        return [self.address1, self.address2]
