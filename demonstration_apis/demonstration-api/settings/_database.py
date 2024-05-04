import os

from sqlalchemy.engine.url import URL


class AbstarctDataBaseConnectionMeta:
    drivername = "mysql+mysqldb"
    username = "stnduser1"
    password = "stnduser1"
    host = "0.0.0.0"
    port = 3306

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
    database = 'demo'


class DevDataBaseConnection(AbstarctDataBaseConnectionMeta):
    database = 'demo'


class DevProxyDataBaseConnection(AbstarctDataBaseConnectionMeta):
    port = 6033
    database = 'demo'
