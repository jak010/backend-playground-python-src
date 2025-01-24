import time
from abc import abstractmethod, ABC, ABCMeta
from dataclasses import dataclass, field
import uuid


class Event(ABCMeta):
    event_id: str
    time: int
    cart_id: int


@dataclass
class ItemAdded:
    event_id: str
    produt_no: int
    product_name: str
    quantity: int
    time: int

    @classmethod
    def of(cls, produt_no: int, product_name: str, quantity: int):
        return cls(
            event_id=str(uuid.uuid4()),
            produt_no=produt_no,
            product_name=product_name,
            quantity=quantity,
            time=int(time.time())
        )


@dataclass
class QuantityChanged:
    event_id: str
    produt_no: int
    quantity: int
    time: int

    @classmethod
    def of(cls, produt_no: int, quantity: int):
        return cls(
            event_id=str(uuid.uuid4()),
            produt_no=produt_no,
            quantity=quantity,
            time=int(time.time())
        )


@dataclass
class ItemRemoved:
    event_id: str
    produt_no: int
    time: int

    @classmethod
    def of(cls, produt_no: int):
        return cls(
            event_id=str(uuid.uuid4()),
            produt_no=produt_no,
            time=int(time.time())
        )
