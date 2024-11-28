from enum import Enum


class DataBaseSettings(Enum):
    host = '127.0.0.1'
    port = 18501
    user = 'root'
    password = '1234'
    database = 'legacy_dsp_db'

    @classmethod
    def get_url_connection(cls):
        return f"mysql+pymysql://{cls.user.value}:{cls.password.value}@{cls.host.value}:{cls.port.value}/{cls.database.value}"
