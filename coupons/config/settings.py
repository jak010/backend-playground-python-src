from fastapi import FastAPI
import functools
import os
import contextlib
from typing import Callable
from dotenv import load_dotenv
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from config import orm
from config.database import DevDataBaseConnection
from src.entity import CouponEntity, CouponIssueEntity

load_dotenv()

DATABASE = {
    "DB_USER": os.environ["DB_USER"],
    "DB_PASSWORD": os.environ["DB_PASSWORD"],
    "DB_HOST": os.environ["DB_HOST"],
    "DB_PORT": int(os.environ["DB_PORT"]),
    "DB_NAME": os.environ["DB_NAME"]
}

CORE = int(os.cpu_count() / 2) + 1

db_engine = engine.create_engine(
    DevDataBaseConnection.get_url(),
    pool_pre_ping=True,
    pool_recycle=5,
    pool_size=CORE,
    max_overflow=int(CORE / 2),
    pool_timeout=10,
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


def transactional(func: Callable):  # XXX: transactionl 임시구현, 이 방법은 type hint가 적용이 안됨
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            db_session.rollback()
            raise e
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
