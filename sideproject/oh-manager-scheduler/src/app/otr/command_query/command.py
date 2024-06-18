from __future__ import annotations

from typing import List

from src.app.abstarct import AbstractCommandQuery
from src.app.otr.command_query.dto import OTRAuditionDto


class OTRCommand(AbstractCommandQuery):
    insert_sql = """
    INSERT INTO auditions (uid, platform, is_remake, title, content, category, author, reward, link, end_date, created_at, modified_at)
      VALUES (:uid, :platform, :is_remake, :title, :content, :category, :author, :reward, :link, :end_date, :created_at, :modified_at);
    """

    @classmethod
    def save(cls, dto: OTRAuditionDto):
        data = dto.to_dict()
        data.update(uid=dto.vid, platform="OTR", is_remake=False)
        try:
            cls.session.execute(cls.insert_sql, data)
        except Exception as e:
            cls.session.rollback()
        finally:
            cls.session.commit()

    @classmethod
    def saves(cls, dtos: List[OTRAuditionDto]):
        insert_dtos = []
        for dto in dtos:
            data = dto.to_dict()
            data.update(uid=dto.vid, platform="OTR", is_remake=False)
            insert_dtos.append(data)

        cls.session.execute(cls.insert_sql, insert_dtos)
        cls.session.commit()
