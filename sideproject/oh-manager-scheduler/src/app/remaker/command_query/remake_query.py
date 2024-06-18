from __future__ import annotations

import datetime

from src.app.abstarct import AbstractCommandQuery, AbstractLoaderDataType


class RemakerQuery(AbstractCommandQuery):

    @classmethod
    def get_by_remake(cls, is_remake: bool) -> AbstractLoaderDataType:
        sql = "SELECT * FROM auditions WHERE is_remake=:is_remake AND :now <= end_date ORDER BY id ASC LIMIT 0,3;"

        params = {
            'is_remake': is_remake,
            "now": datetime.datetime.now()
        }

        result = cls.session.execute(sql, params).mappings().all()
        cls.session.commit()

        if result:
            return result
