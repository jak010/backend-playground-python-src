from dataclasses import dataclass


@dataclass
class CreateCart:
    cart_id: str


class Evenet: ...


@dataclass
class CartCreate(Evenet):
    cart_id: str


class Cart:
    cart_id: str
    deleted: bool

    def __init__(self, command: CreateCart):
        self.apply(CartCreate(command.cart_id))

    def on(self, event: CartCreate):
        self.cart_id = event.cart_id

    def mark_deleted(self):
        self.deleted = True


class CartRepository:
    pass


class CartStore:
    cart_repositroy: CartRepository

    def exists(self, cart_id):
        return self.cart_repositroy.existsBy(cart_id)


class CartService:
    cart_store: CartStore

    def create_cart(self, command: CreateCart):
        if self.cart_store.exists(command.cart_id):
            raise Exception("Cart already exists")

        cart = Cart(command)
        self.cart_store.save(cart)
