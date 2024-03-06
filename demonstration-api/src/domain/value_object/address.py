import dataclasses
from abc import ABCMeta
import json


@dataclasses.dataclass(frozen=True)
class AbstractValueObject(metaclass=ABCMeta):

    def __str__(self):
        return f"{self.__class__.__name__}({json.dumps(dataclasses.asdict(self))})"

    def __ne__(self, other):
        return not self.__eq__(other)

    def __composite_values__(self): ...


@dataclasses.dataclass(frozen=True, eq=True)
class Address(AbstractValueObject):
    address1: str
    address2: str

    def __composite_values__(self):
        return [self.address1, self.address2]
