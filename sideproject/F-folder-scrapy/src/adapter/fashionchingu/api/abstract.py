from abc import ABCMeta, abstractmethod
from typing import List

from src.adapter.utils import RequestMixin


class AbstractApiInterface(RequestMixin, metaclass=ABCMeta):

    @abstractmethod
    def get_links(self, page) -> List[str]: ...

    @abstractmethod
    def emit(self, *args, **kwargs) -> List[str]: ...
