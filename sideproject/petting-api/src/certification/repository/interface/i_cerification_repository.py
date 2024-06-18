from __future__ import annotations

from abc import abstractmethod, ABC

from src.certification.entity import CeritifcationEntity


class ICerificationRepository(ABC):

    @abstractmethod
    def add(self, cerification_entity: CeritifcationEntity) -> CeritifcationEntity: ...

    @abstractmethod
    def find_by_nanoid(self, nanoid: str) -> CeritifcationEntity: ...
