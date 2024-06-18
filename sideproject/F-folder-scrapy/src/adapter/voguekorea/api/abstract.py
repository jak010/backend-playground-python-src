from abc import ABCMeta, abstractmethod

from fake_useragent import UserAgent

from src.adapter.utils import RequestMixin
from src.adapter.voguekorea.api.libs.dto import FashionTrends


class AbstractApiInterface(RequestMixin, metaclass=ABCMeta):
    HOST = None
    USER_AGENT = UserAgent().random

    @abstractmethod
    def get_fashion_trends(self, page: int, item_per_page: int) -> FashionTrends: ...
