import os

from dotenv import load_dotenv

from sqlalchemy import engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()

DATABASE = {
    "DB_USER": os.environ["DB_USER"],
    "DB_PASSWORD": os.environ["DB_PASSWORD"],
    "DB_HOST": os.environ["DB_HOST"],
    "DB_PORT": int(os.environ["DB_PORT"]),
    "DB_NAME": os.environ["DB_NAME"]
}

url = URL.create(
    drivername="mysql+pymysql://",
    username=DATABASE["DB_USER"],
    password=DATABASE["DB_PASSWORD"],
    database=DATABASE["DB_NAME"],
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

db_session = scoped_session(sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
))
