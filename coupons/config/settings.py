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

CORE = int(os.cpu_count())

db_engine = engine.create_engine(
    DevDataBaseConnection.get_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=CORE,
    max_overflow=CORE * 2,
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
            db_session.commit()
            db_session.close()
            return result
        except CouponIssueException as e:
            db_session.rollback()  # XXX: exception이 터질 때는 rollback 처리, 안 그러면 다른 트랜잭션에서 대기하는 경우가 발생함
            raise e

    return _wrapper


from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    registry = bootstrapping()

    yield

    print("[FASTAPI] END ")
    registry.dispose()
    db_session.close_all()
