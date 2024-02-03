import os
import contextlib
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

db_engine = engine.create_engine(
    DevDataBaseConnection.get_url(),
    pool_pre_ping=True,
    pool_recycle=5,
    pool_size=5,
    pool_timeout=15
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
