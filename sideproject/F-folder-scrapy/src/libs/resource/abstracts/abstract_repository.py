from abc import ABCMeta, abstractmethod

from sqlalchemy import text
from sqlalchemy.engine.result import MappingResult
from sqlalchemy.orm.session import Session


class NotExistEntity(Exception):
    """Entity가 존재하지 않는다."""


class AbstractRepository(metaclass=ABCMeta):
    TABLE_NAME = None

    def __init__(self, session):
        self._session: Session = session

    @abstractmethod
    def add(self, *args, **kwargs):
        ...

    def update(self, *args, **kwargs):
        ...

    def find_by(self, *args, **kwargs):
        ...

    def _execute(self, sql: str, params: dict = None) -> MappingResult:
        return self._session.execute(text(sql), params).mappings()

    def _executemany(self, sql: str, params: list[dict]):
        for param in params:
            self._session.execute(text(sql), param)

    def get_page_limit(self, page: int, item_per_page: int):
        return (page - 1) * item_per_page

    def get_count(self):
        sql = f"SELECT COUNT(`id`) as count FROM `{self.TABLE_NAME}`;"

        query = self._execute(sql).fetchone()

        if query is not None:
            return query['count']
        return 0
