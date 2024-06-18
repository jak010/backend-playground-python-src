from abc import ABCMeta


class AbstractUseCase(metaclass=ABCMeta):

    def execute(self, *args, **kwrags): ...
