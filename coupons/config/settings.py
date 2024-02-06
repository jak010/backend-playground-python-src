import functools
import os
from typing import Callable

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from config import orm
from config.database import DevDataBaseConnection
from src.entity import CouponEntity, CouponIssueEntity
from src.exceptions import CouponIssueException

load_dotenv()

DATABASE = {
    "DB_USER": os.environ["DB_USER"],
    "DB_PASSWORD": os.environ["DB_PASSWORD"],
    "DB_HOST": os.environ["DB_HOST"],
    "DB_PORT": int(os.environ["DB_PORT"]),
    "DB_NAME": os.environ["DB_NAME"]
}

CORE = int(os.cpu_count() / 2)

db_engine = engine.create_engine(
    DevDataBaseConnection.get_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=CORE,
    max_overflow=CORE + 1,
    pool_timeout=30,
    echo=True
)

db_session: Session = scoped_session(sessionmaker(
    bind=db_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
))


def bootstrapping():
    from sqlalchemy.orm import registry
    orm_mapping = registry()
    orm_mapping.map_imperatively(CouponEntity, orm.Coupon)
    orm_mapping.map_imperatively(CouponIssueEntity, orm.CouponIssue)
    return orm_mapping


def transactional(func: Callable):  # XXX: transactionl 임시구현, 이 방법(decorator)은 type hint가 적용이 안됨
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except CouponIssueException as e:
            db_session.commit()
        finally:
            db_session.commit()
            db_session.close()

    return _wrapper


from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_session.execute("select 1;")  # session bump

    registry = bootstrapping()

    yield

    registry.dispose()
