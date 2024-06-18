from __future__ import annotations

from src.adapter.abstract.abstract_dto import AbstractDto


class FashionInsightDto(AbstractDto):

    @classmethod
    def new(
            cls,
            *,
            id=None,
            trace_id=None,
            reference_id=None,
            reference_date=None,
            reference_link=None,
            title=None,
            content=None,
            thumbnail=None
    ):
        return cls(
            id=id,
            trace_id=trace_id,
            reference_id=reference_id,
            reference_date=reference_date,
            reference_link=reference_link,
            title=title,
            content=content,
            thumbnail=thumbnail
        )
