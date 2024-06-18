from src.adapter.utils import RequestMixin
from abc import ABCMeta, abstractmethod
from typing import List


class AbstractApiInterface(RequestMixin, metaclass=ABCMeta):

    @abstractmethod
    def get_links(self, page) -> List[str]: ...

    @abstractmethod
    def emit(self, *args, **kwargs) -> List[str]: ...
