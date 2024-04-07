import os
from enum import Enum

from dotenv import load_dotenv

from sqlalchemy.engine import URL

load_dotenv()


class TMDBConfiguration(Enum):
    TMDB_API_READ_KEY = os.environ['TMDB_API_READ_KEY']


class DataBaseConfiguration(Enum):
    DB_DRIVER = os.environ['DB_DRIVER']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_NAME = os.environ['DB_NAME']
    DB_PORT = os.environ['DB_PORT']
    DB_HOST = os.environ['DB_HOST']

    @classmethod
    def get_db_url(cls):
        return URL.create(
            drivername=cls.DB_DRIVER.value,
            username=cls.DB_USER.value,
            password=cls.DB_PASSWORD.value,
            database=cls.DB_NAME.value,
            host=cls.DB_HOST.value,
            port=int(cls.DB_PORT.value)
        )
