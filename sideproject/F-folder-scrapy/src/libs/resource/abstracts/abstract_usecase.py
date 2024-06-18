import uuid
from abc import ABCMeta, abstractmethod
from typing import List, Optional, Dict, Generic, TypeVar, Tuple, Union

from dependency_injector.wiring import Provide
from sqlalchemy.orm import Session

from src.config.container.context import ContextContainer
from src.config.container.database import RepositoryContainer
from src.libs.resource.eyesmag.eyesmag_repository import EyesMagRepository
from src.libs.resource.fashionchingu.fashionchingu_repository import FashionChinguRepository
from src.libs.resource.fashioninsight.fashioninsight_repository import FashionInsightRepository
from src.libs.resource.harpersbazaar.harpersbazaar_repository import HarpersBazaarRepository
from src.libs.resource.kmodes.kmodes_repository import KmodesRepository
from src.libs.resource.krazefashion.krazefashion_repository import KrazeFashionRepository
from src.libs.resource.krazemedia.krazemedia_repository import KrazeMediaRepository
from src.libs.resource.post.post_history_repository import PostHistoryRepository
from src.libs.resource.post.post_repository import PostRepository
from src.libs.resource.unnielooks.unnielooks_repository import UnnieLooksRepository
from src.libs.resource.voguekorea.voguekorea_repository import VogueKoreaRepository
from src.libs.resource.yesstyle.yesstyle_repository import YesstyleRepository

T = TypeVar("T")


class AbstractUsecase(metaclass=ABCMeta):
    session: Session = Provide[ContextContainer.session]
    post_repository: PostRepository = Provide[RepositoryContainer.post_repository]
    voguekorea_repository: VogueKoreaRepository = Provide[RepositoryContainer.voguekorea_repository]
    fashionchingu_repository: FashionChinguRepository = Provide[RepositoryContainer.fashionchingu_repository]
    eyesmag_repository: EyesMagRepository = Provide[RepositoryContainer.eyesmag_repository]
    fashioninsight_repository: FashionInsightRepository = Provide[RepositoryContainer.fashioninsight_repository]
    unnielooks_repository: UnnieLooksRepository = Provide[RepositoryContainer.unnielooks_repository]
    yesstyle_repository: YesstyleRepository = Provide[RepositoryContainer.yesstyle_repository]
    harpersbazaar_repository: HarpersBazaarRepository = Provide[RepositoryContainer.harpersbazaar_repository]
    kmodes_repository: KmodesRepository = Provide[RepositoryContainer.kmodes_repository]
    krazefashion_repository: KrazeFashionRepository = Provide[RepositoryContainer.krazefashion_repository]
    krazemedia_repository: KrazeMediaRepository = Provide[RepositoryContainer.krazemedia_repository]
    post_history_repository: PostHistoryRepository = Provide[RepositoryContainer.post_history_repository]


class AbstractUsecaseCRUDImplements(Generic[T]):

    @abstractmethod
    def get_content_list(self, *args, **kwargs) -> Optional[Tuple[List[T], int]]: ...

    @abstractmethod
    def get_content(self, *args, **kwargs) -> Optional[T]: ...

    def get_count(self) -> int: ...

    def update_by(self, *args, **kwargs) -> int: ...


class AbstrctUsecaseCrawlerImplements:

    @abstractmethod
    def convert(self, trace_id: Union[str, uuid.UUID]) -> Dict[str, str]: ...

    @abstractmethod
    def daily_collect(self): ...

    def all_collect(self): ...
