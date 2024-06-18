from __future__ import annotations

import uuid
from typing import List, Optional, Tuple

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.common.universal_entity import UniversalEntity


class HarpersBazaarRepository(AbstractRepository):
    TABLE_NAME = "harpersbazaar"

    insert_sql = f"INSERT INTO `{TABLE_NAME}` (" \
                 " trace_id," \
                 " is_convert," \
                 " reference_id," \
                 " reference_date," \
                 " reference_link," \
                 " title," \
                 " content," \
                 " thumbnail" \
                 ") VALUES (" \
                 ":trace_id," \
                 ":is_convert," \
                 ":reference_id," \
                 ":reference_date," \
                 ":reference_link," \
                 ":title," \
                 ":content," \
                 ":thumbnail" \
                 ");"

    def add(self, universal_entity: UniversalEntity):
        self._execute(self.insert_sql, universal_entity.to_dict())

    def update(self, *args, **kwargs):
        pass

    def update_on_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        update_sql = f"UPDATE {self.TABLE_NAME} SET" \
                     f" is_convert=:is_convert" \
                     f" WHERE trace_id=:trace_id;"
        params = {"trace_id": trace_id, "is_convert": is_convert.value}
        self._execute(update_sql, params)

    def find_by(
            self,
            page: int = None,
            item_per_page: int = None,
            sort_key: str = None,
            sort_type: str = None

    ) -> Tuple[Optional[List[UniversalEntity]], int]:
        sql = f"SELECT * FROM {self.TABLE_NAME}"
        paginate_sql = f" ORDER BY `{sort_key}` {sort_type} LIMIT {(page - 1) * item_per_page}, {item_per_page};"
        items = self._execute(sql + paginate_sql).fetchall()

        count_sql = f"SELECT count(`id`) as total_count FROM {self.TABLE_NAME};"
        count = self._execute(count_sql).fetchone()

        objs = []
        for item in items:
            objs.append(UniversalEntity(**item))

        return objs, count['total_count']

    def find_by_trace_id(self, trace_id: str) -> UniversalEntity:
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE trace_id =:trace_id;"
        params = {"trace_id": trace_id}

        result = self._execute(sql, params).fetchone()
        if result:
            return UniversalEntity(**result)

    def find_by_refernece_id(self, reference_id: int) -> UniversalEntity:
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE reference_id =:reference_id;"
        params = {"reference_id": reference_id}

        result = self._execute(sql, params).fetchone()
        if result:
            return UniversalEntity(**result)

    def find_by_refernece_ids(self, reference_ids: list[int]) -> Optional[List[UniversalEntity]]:
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE reference_id IN :reference_ids;"
        params = {"reference_ids": reference_ids}

        results = self._execute(sql, params).fetchall()

        objs = []
        for result in results:
            objs.append(UniversalEntity(**result))
        return objs
