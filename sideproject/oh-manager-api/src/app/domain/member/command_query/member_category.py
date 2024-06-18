from __future__ import annotations
import dataclasses
import time

from dependency_injector.wiring import Provide
from sqlalchemy.orm import Session

from src.config.container.database_container import DataBaseContainer
from src.app.domain.abstract import AbstractCommandQuery
from typing import List
from sqlalchemy.exc import IntegrityError


class MemberCategoryDuplicateError(Exception):
    """ Member Category 중복 """


@dataclasses.dataclass
class MemberCategoryMapper:
    id: int = dataclasses.field()
    member_id: str = dataclasses.field()
    primary: str = dataclasses.field()
    secondary: str = dataclasses.field()
    created_at: int = dataclasses.field()
    modified_at: int = dataclasses.field()

    def to_dict(self):
        exclude_fields = ["member_id"]
        data = dataclasses.asdict(self)

        for exclude_field in exclude_fields:
            data.pop(exclude_field)

        return data


class MemberCategoryQuery(AbstractCommandQuery):

    @classmethod
    def find_by(cls, member_id: str) -> List[MemberCategoryMapper]:
        sql = "SELECT * FROM member_category WHERE member_id=:member_id;"
        params = {"member_id": member_id}

        result = []
        for row in cls.session.execute(sql, params).mappings().all():
            result.append(MemberCategoryMapper(**row))
        return result


class MemberCategoryCommand(AbstractCommandQuery):
    session: Session = Provide[DataBaseContainer.session]

    @classmethod
    def insert(cls, member_id: str, primary: str, secondary: str = ''):
        sql = "INSERT INTO member_category (`member_id`, `primary`, `secondary`, `created_at`, `modified_at`)" \
              " VALUES (:member_id, :primary, :secondary, :created_at, :modified_at);"
        params = {
            "member_id": member_id,
            "primary": primary,
            "secondary": secondary if secondary is not None else '',
            "created_at": int(time.time()),
            "modified_at": int(time.time())
        }
        try:
            cls.session.execute(sql, params)
        except IntegrityError:
            raise MemberCategoryDuplicateError()
