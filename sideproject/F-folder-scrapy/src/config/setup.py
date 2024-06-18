from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy.orm import registry

from src.application.routers import (
    entry_router,
    post_router,
    voguekorea_router,
    fashionchingu_rotuer,
    eyesmag_rotuer,
    fashioninsight_rotuer,
    unnielooks_router,
    yesstyle_rotuer,
    kmodes_rotuer,
    krazefashion_rotuer,
    krazemedia_rotuer,
    harpersbazaar_rotuer
)
from src.config.container.context import ContextContainer
from src.config.container.database import RepositoryContainer
from src.libs.resource.eyesmag.eyesmag_entity import EyesMagEntity
from src.libs.resource.fashionchingu.fashiochingu_entity import FashionChinguEntity
from src.libs.resource.fashioninsight.fashioninsight_entity import FashionInsightEntity
from src.libs.resource.kmodes.kmodes_entity import KmodesEntity
from src.libs.resource.krazefashion.krazefashion_entity import KrazeFashionEntity
from src.libs.resource.krazemedia.krazemedia_entity import KrazeMediaEntity
from src.libs.resource.post.post_entity import PostEntity
from src.libs.resource.post.post_history_entity import PostHistoryEntity
from src.libs.resource.unnielooks.unnielooks_entity import UnnielooksEntity
from src.libs.resource.voguekorea.voguekorea_entity import VogueKoreaEntity

load_dotenv()


def add_controller(app: FastAPI):
    for router in [
        entry_router,
        post_router,
        voguekorea_router,
        fashionchingu_rotuer,
        eyesmag_rotuer,
        fashioninsight_rotuer,
        unnielooks_router,
        yesstyle_rotuer,
        kmodes_rotuer,
        krazefashion_rotuer,
        krazemedia_rotuer,
        harpersbazaar_rotuer
    ]:
        app.include_router(router)


def add_database(db: dict):
    from sqlalchemy.engine import URL, create_engine

    engine = create_engine(
        URL.create(
            drivername="mysql+pymysql",
            username=db['username'],
            password=db['password'],
            database=db['database'],
            host=db['host'],
            port=int(db['port'])
        ),
        pool_pre_ping=True,
        pool_recycle=5,
        pool_size=5,
        pool_timeout=15,
        echo=True
    )

    context = ContextContainer(engine=engine)
    context.wire(packages=["src.libs", "src.config"])

    repository_conatiner = RepositoryContainer(session=context.session)
    repository_conatiner.wire(packages=["src.libs", "src.config"])


def orm_dispatch():
    from src.adapter.database.orm import (
        Voguekorea,
        Fashionchingu,
        Eyesmag,
        Kmode,
        Krazefashion,
        Krazemedia,
        Post,
        PostHistory,
        Fashioninsight,
        Unnielook
    )

    mapper_registry = registry()
    mapper_registry.map_imperatively(VogueKoreaEntity, Voguekorea)
    mapper_registry.map_imperatively(FashionChinguEntity, Fashionchingu)
    mapper_registry.map_imperatively(EyesMagEntity, Eyesmag)
    mapper_registry.map_imperatively(KmodesEntity, Kmode)
    mapper_registry.map_imperatively(KrazeFashionEntity, Krazefashion)
    mapper_registry.map_imperatively(KrazeMediaEntity, Krazemedia)
    mapper_registry.map_imperatively(PostEntity, Post)
    mapper_registry.map_imperatively(PostHistoryEntity, PostHistory)
    mapper_registry.map_imperatively(FashionInsightEntity, Fashioninsight)
    mapper_registry.map_imperatively(UnnielooksEntity, Unnielook)
