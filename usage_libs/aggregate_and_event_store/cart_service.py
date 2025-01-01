from cart_store import CartStore


class CartService:
    cart_stroe = CartStore()

    def add_item(self,
                 cart_id: str,
                 product_no: str,
                 product_name: str,
                 quantity: int
                 ):
        cart = self.cart_stroe.load(cart_id)
        cart.add_item(product_no, product_name, quantity)
        self.cart_stroe.save(cart)

    def change_quantity(self,
                        cart_id: str,
                        product_no: str,
                        quantity: int
                        ):
        cart = self.cart_stroe.load(cart_id)
        cart.change_quantity(product_no, quantity)
        self.cart_stroe.save(cart)

    def remove_item(self,
                    cart_id: str,
                    product_no: str
                    ):
        cart = self.cart_stroe.load(cart_id)
        cart.remove_item(product_no)
        self.cart_stroe.save(cart)
