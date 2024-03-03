from abc import abstractmethod, ABCMeta


class Stack(ABCMeta):
    name: str

    @abstractmethod
    def size(self): ...


class SubStack1(Stack):

    def size(self): print("SubStack1")


class SubStack2(Stack):
    def size(self): print("SubStack1")
