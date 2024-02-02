import os

from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

load_dotenv()


class AbstarctDataBaseConnectionMeta:
    drivername = "mysql+mysqldb"
    username = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    host = os.environ["DB_HOST"]
    port = int(os.environ["DB_PORT"])

    database = None

    @classmethod
    def get_url(cls):
        return URL.create(
            drivername=cls.drivername,
            username=cls.username,
            password=cls.password,
            database=cls.database,
            host=cls.host,
            port=cls.port
        )


class TestDataBaseConnection(AbstarctDataBaseConnectionMeta):
    database = 'test_coupons'


class DevDataBaseConnection(AbstarctDataBaseConnectionMeta):
    database = 'coupons'
