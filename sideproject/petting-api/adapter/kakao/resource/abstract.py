from abc import ABCMeta

from adapter.kakao.libs.config import KaKaoConfig as _KaKaoConfig


class AbstractKaKaoResource(metaclass=ABCMeta):

    def __init__(self, config: _KaKaoConfig):
        self.config = config
