import os
from enum import Enum
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()


class DataBaseEnviroment(Enum):
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']
    DB_NAME = os.environ['DB_NAME']

    @classmethod
    def get_uri(cls):
        return URL.create(
            drivername="mysql+mysqldb",
            username=cls.DB_USER.value,
            password=cls.DB_PASSWORD.value,
            database=cls.DB_NAME.value,
            host=cls.DB_HOST.value,
            port=int(cls.DB_PORT.value)
        )
