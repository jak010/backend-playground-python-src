from functools import cached_property
import pymysql


class Context:

    def __init__(self):
        self.conn = pymysql.connect(
            user='root',
            password='1234',
            host="127.0.0.1",
            port=9902,
            database="playground",
        )

    @cached_property
    def cursor(self):
        return self.conn.cursor(pymysql.cursors.DictCursor)

    def close(self):
        return self.conn.close()

    def commit(self):
        return self.conn.commit()

    def rollback(self):
        return self.conn.rollback()
