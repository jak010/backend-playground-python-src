from abc import ABCMeta

# DIP ?

class IRepositry(metaclass=ABCMeta):

    def get(self): ...


class SomeRepository(IRepositry): ...


class SomeService:

    def __init__(self):
        self.some_repository: IRepositry = SomeRepository()

    def method(self):
        self.some_repository.get()
