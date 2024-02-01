import os

from dotenv import load_dotenv
from sqlalchemy import engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from config import orm
from src.entity import CouponEntity, CouponIssueEntity

load_dotenv()

DATABASE = {
    "DB_USER": os.environ["DB_USER"],
    "DB_PASSWORD": os.environ["DB_PASSWORD"],
    "DB_HOST": os.environ["DB_HOST"],
    "DB_PORT": int(os.environ["DB_PORT"]),
    "DB_NAME": os.environ["DB_NAME"]
}

url = URL.create(
    drivername="mysql+mysqldb",
    username=DATABASE["DB_USER"],
    password=DATABASE["DB_PASSWORD"],
    database=DATABASE["DB_NAME"],
    host=DATABASE["DB_HOST"],
    port=int(DATABASE["DB_PORT"])
)
test_url = URL.create(
    drivername="mysql+mysqldb",
    username=DATABASE["DB_USER"],
    password=DATABASE["DB_PASSWORD"],
    database='test_coupons',
    host=DATABASE["DB_HOST"],
    port=int(DATABASE["DB_PORT"])
)

db_engine = engine.create_engine(
    url,
    pool_pre_ping=True,
    pool_recycle=5,
    pool_size=5,
    pool_timeout=15,
    echo=True,
)

db_session: Session = scoped_session(sessionmaker(
    bind=db_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
))


def bootstrapping():
    from sqlalchemy.orm import registry, mapper
    orm_mapping = registry()
    orm_mapping.map_imperatively(CouponEntity, orm.Coupon)
    orm_mapping.map_imperatively(CouponIssueEntity, orm.CouponIssue)
    return orm_mapping
