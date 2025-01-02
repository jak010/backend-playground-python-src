from dataclasses import dataclass


@dataclass
class AddItem:
    cart_id: str
    product_no: str
    product_name: str
    quantity: int


@dataclass
class ChangeQuantity:
    cart_id: str
    product_no: str
    quantity: int

    def validate(self):
        if self.cart_id is None:
            raise Exception("cart_id cannot be None.")
        if self.quantity <= 0:
            raise Exception("quantity must be greater than 0.")


@dataclass
class RemoveItem:
    cart_id: str
    product_no: str
