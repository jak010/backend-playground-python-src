from abc import ABCMeta, abstractmethod

from fake_useragent import UserAgent

from src.adapter.utils import RequestMixin


class AbstractApiInterface(RequestMixin, metaclass=ABCMeta):
    HOST = None
    USER_AGENT = UserAgent().random
