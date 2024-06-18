from __future__ import annotations

from typing import Optional

from src.app.abstarct import AbstractCommandQuery, AbstractLoaderDataType


class EntityDoesNotExist(Exception):
    """ Not Exist Entity.. """


class OTRQuery(AbstractCommandQuery):

    @classmethod
    def get_by_id(cls, vid: int) -> AbstractLoaderDataType:
        sql = "SELECT * FROM auditions WHERE uid=:vid;"
        params = {"vid": vid}
        result = cls.session.execute(sql, params).mappings().first()
        cls.session.commit()

        if result:
            return result
        raise EntityDoesNotExist()

    @classmethod
    def find_by_id(cls, vid: int) -> AbstractLoaderDataType:
        sql = "SELECT * FROM auditions WHERE uid=:vid;"
        params = {"vid": vid}
        result = cls.session.execute(sql, params).mappings().one_or_none()
        cls.session.commit()
        return result

    @classmethod
    def get_latest(cls) -> AbstractLoaderDataType:
        sql = "SELECT * FROM auditions ORDER BY uid DESC LIMIT 0, 25;"
        result = cls.session.execute(sql).mappings().all()
        cls.session.commit()

        if result:
            return result

    @classmethod
    def exist(cls, vid: int) -> Optional[AbstractLoaderDataType]:
        sql = "SELECT * FROM auditions " \
              " WHERE uid=:vid AND platform=:platform;"
        params = {
            "vid": vid,
            "platform": "OTR"
        }
        result = cls.session.execute(sql, params).mappings().first()
        cls.session.commit()

        if result:
            return result
        return None
