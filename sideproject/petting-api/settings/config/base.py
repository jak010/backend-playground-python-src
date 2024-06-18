import os
from enum import Enum

from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

load_dotenv()

TOKEN_SCRET = os.environ['APPLICATION_SECRET']


class AWSConfig(Enum):
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_ACCESS_SECRET_KEY = os.environ['AWS_ACCESS_SECRET_KEY']
    AWS_REGION_NAME = os.environ['AWS_REGION_NAME']

    AWS_S3_BUCKET = os.environ['AWS_S3_BUCKET']


class KaKaoConfig(Enum):
    CLIENT_ID = os.environ['KAKAO_CLIENT_ID']
    CLIENT_SECRET = os.environ['KAKAO_CLIENT_SECRET']
    REDIRECT_URL = os.environ['KAKAO_CLIENT_REDIRECT_URL']


class AligoConfig(Enum):
    ALIGO_API_KEY = os.environ['ALIGO_API_KEY']
    ALIGO_USER_ID = os.environ['ALIGO_USER_ID']
    ALIGO_SENDER = os.environ['ALIGO_SENDER']


class DBConfig:
    DB_DRIVER: str = os.environ['DB_DRIVER']
    DB_USER: str = os.environ['DB_USER']
    DB_PASSWORD: str = os.environ['DB_PASSWORD']
    DB_NAME: str = os.environ['DB_NAME']
    DB_PORT: int = os.environ['DB_PORT']
    DB_HOST: str = os.environ['DB_HOST']

    @classmethod
    def get_driver(cls):
        if cls.DB_DRIVER == '' or cls.DB_DRIVER is None:
            raise Exception("DB Driver Not Setting")

        return URL.create(
            drivername=cls.DB_DRIVER,
            username=cls.DB_USER,
            password=cls.DB_PASSWORD,
            database=cls.DB_NAME,
            host=cls.DB_HOST,
            port=cls.DB_PORT
        )


class ExecuteEnviorment:
    MODE = os.environ['MODE']

    @property
    def get_database_url(self) -> str:
        return DBConfig.get_driver()
