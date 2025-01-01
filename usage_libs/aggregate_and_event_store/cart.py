from dataclasses import dataclass
from typing import List

from .events import ItemAdded, ItemRemoved, QuantityChanged


@dataclass
class Item:
    item_id: str
    product_no: str
    product_name: str
    price: int
    quantity: int


class Cart:

    def __init__(self, cart_id: str):
        self._cart_id: str = cart_id
        self._items: list = []
        self.events: List[object] = []

    def add_item(self, product_no: str, product_name: str, quantity: int):
        self._items.append(Item(product_no, product_name, quantity))

        self.events.append(ItemAdded.of(product_no, product_name, quantity))

    def change_quantity(self, product_no: str, quantity: int):
        if not self._items:
            return

        for item in self._items:
            if item.product_no == product_no:
                item.quantity = quantity

        self.events.append(QuantityChanged.of(product_no, quantity))

    def remove_item(self, product_no: str):
        if not self._items:
            return

        for item in self._items:
            if item.product_no == product_no:
                self._items.remove(item)

        self.events.append(ItemRemoved.of(product_no))
