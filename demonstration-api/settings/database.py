import os

from sqlalchemy.engine.url import URL


class AbstarctDataBaseConnectionMeta:
    drivername = "mysql+mysqldb"
    username = "demo"
    password = "1234"
    host = "127.0.0.1"
    port = 19501

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
    database = 'test_demo'


class DevDataBaseConnection(AbstarctDataBaseConnectionMeta):
    database = 'demo'
