from __future__ import annotations

from typing import Union

from src.libs.resource.abstracts.abstract_usecase import AbstractUsecaseCRUDImplements, AbstrctUsecaseCrawlerImplements
from src.libs.resource.common.universal_entity import UniversalEntity

USECASE_TYPE = Union[AbstractUsecaseCRUDImplements[UniversalEntity], AbstrctUsecaseCrawlerImplements]
