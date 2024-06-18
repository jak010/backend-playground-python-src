from __future__ import annotations

from abc import ABCMeta, abstractmethod

from typing import List, Any


class AbstractScrapPipeLine(metaclass=ABCMeta):

    def __init__(self, init_filter):
        self.filters: List[AbstractScrapFilter] = [init_filter]
        self._data = None

    def append_filter(self, pipe_fileter):
        self.filters.append(pipe_fileter)

    @abstractmethod
    def start(self) -> Any: ...

    def get_result(self):
        return ''.join(self._data)

    def get_data(self):
        return self._data

    def get_dict(self) -> dict:
        return self._data


class AbstractScrapFilter(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, *arg, **kwargs): ...
