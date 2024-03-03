from abc import abstractmethod

from typing import TypeVar, Protocol, Generic, Annotated

T = TypeVar("T", contravariant=True)


class Interface(Protocol[T]):

    def hello(self):
        print("???")


class ConcreateInterface(Interface[T]):

    def session(self):
        return "Hello, Sessiona"


class Action(ConcreateInterface[Interface]):

    def hello(self):
        print(self.session())


if __name__ == '__main__':
    a = Action()
    # print(a.session())
    a.hello()
