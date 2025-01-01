from abc import ABC, ABCMeta, abstractmethod

from .cart import Cart


class CartStore(ABC, metaclass=ABCMeta):

    @abstractmethod
    def save(self, cart: Cart):
        pass

    @abstractmethod
    def load(self, cart_id: str):
        pass
