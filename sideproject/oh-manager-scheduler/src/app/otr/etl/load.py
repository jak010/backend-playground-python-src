from __future__ import annotations

from typing import List

from src.app.abstarct import AbstractLoaderDataType
from src.app.otr.command_query.dto import OTRAuditionDto
from src.app.otr.command_query import OTRQuery


class OTRLoader:
    query = OTRQuery()

    @classmethod
    def fetch_data_for_storage(cls, latest_saved_data: List[AbstractLoaderDataType], latest_fetch_data: List[OTRAuditionDto]) -> List[OTRAuditionDto]:
        """DataBase에 없는 데이터 찾기"""
        if latest_saved_data is None:
            return latest_fetch_data

        latest_uids = set([int(data['uid']) for data in latest_saved_data])  # db.uid
        load_uids = set([int(dto.vid) for dto in latest_fetch_data])  # dto.vid

        needs_saved_uids = load_uids - latest_uids

        if needs_saved_uids is None:
            return []

        saved_uids = []
        for needs_saved_uid in needs_saved_uids:
            if cls.query.find_by_id(vid=needs_saved_uid) is None:
                saved_uids.append(needs_saved_uid)

        result = []
        for dto in latest_fetch_data:
            if int(dto.vid) in saved_uids:
                result.append(dto)

        return result
