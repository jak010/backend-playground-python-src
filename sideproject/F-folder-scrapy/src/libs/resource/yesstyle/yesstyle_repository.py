from __future__ import annotations

import uuid
from typing import Optional, List, Tuple

from src.libs.resource.abstracts.abstract_repository import AbstractRepository
from src.libs.resource.common import define
from src.libs.resource.common.universal_entity import UniversalEntity


class YesstyleRepository(AbstractRepository):
    TABLE_NAME = "yesstyle"

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

    def add(self, unversal_entity: UniversalEntity):
        self._execute(self.insert_sql, unversal_entity.to_dict())

    def update(self, *args, **kwargs):
        pass

    def update_on_convert(self, trace_id: uuid.UUID, is_convert: define.CONVERT):
        update_sql = f"UPDATE {self.TABLE_NAME} SET" \
                     f" is_convert=:is_convert" \
                     f" WHERE trace_id=:trace_id;"
        params = {"trace_id": trace_id, "is_convert": is_convert.value}
        self._execute(update_sql, params)

    def find_by(self,
                sort_key: str = None,
                sort_type: str = None,
                page: int = None,
                item_per_page: int = None
                ) -> Tuple[Optional[List[UniversalEntity]], int]:
        sql = "SELECT *" \
              f" FROM `{self.TABLE_NAME}`" \
              f" ORDER BY {sort_key}, `id` {sort_type}" \
              f" LIMIT {item_per_page} OFFSET {self.get_page_limit(page, item_per_page)}"
        count_sql = f"SELECT COUNT(`id`) as count FROM {self.TABLE_NAME};"

        items = []
        for query in self._execute(sql).fetchall():
            items.append(UniversalEntity(**query))

        count_result = self._execute(count_sql).fetchone()

        return items, count_result['count']

    def find_by_trace_id(self, trace_id: str) -> UniversalEntity:
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE trace_id=:trace_id;"
        params = {"trace_id": trace_id}

        result = self._execute(sql, params).fetchone()
        if result:
            return UniversalEntity(**result)

    def find_by_title(self, title: str) -> UniversalEntity:
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE title=:title;"
        params = {"title": title}

        result = self._execute(sql, params).fetchone()
        if result:
            return UniversalEntity(**result)

    def find_by_titles(self, titles: List[str]) -> Optional[List[UniversalEntity]]:
        sql = f"SELECT * FROM {self.TABLE_NAME} WHERE title IN :titles;"
        params = {"titles": titles}

        objs = []

        result = self._execute(sql, params).fetchall()
        for each in result:
            objs.append(UniversalEntity(**each))

        return objs
