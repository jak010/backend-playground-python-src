from __future__ import annotations

import dataclasses
import datetime
import uuid
from typing import Any, Optional


@dataclasses.dataclass
class UniversalEntity:
    id: Optional[int] = dataclasses.field()
    trace_id: str | uuid.UUID = dataclasses.field(init=True)
    is_convert: int = dataclasses.field(init=True)
    reference_id: Optional[Any] = dataclasses.field(init=True)
    reference_date: str | datetime.date = dataclasses.field(init=True)
    reference_link: str = dataclasses.field(init=True)
    title: str = dataclasses.field(init=True)
    content: str = dataclasses.field(init=True)
    thumbnail: str = dataclasses.field(init=True)

    def __repr__(self):
        return f"\n\nUniversalEntity(id={self.id}\n" \
               f" trace_id={self.trace_id}\n" \
               f" reference_id={self.reference_id}\n" \
               f" reference_date={self.reference_date}\n" \
               f" title={self.title}\n" \
               f" thumbnail={self.thumbnail}\n"

    def to_dict(self):
        return dataclasses.asdict(self)

    @classmethod
    def new(
            cls,
            trace_id=None,
            is_convert=None,
            reference_id: str = None,
            reference_date: str = None,
            reference_link: str = None,
            title: str = None,
            content: str = None,
            thumbnail: str = None

    ):
        return cls(
            id=None,
            trace_id=trace_id if trace_id is not None else uuid.uuid4(),
            is_convert=is_convert if is_convert is not None else 0,
            reference_id=reference_id if reference_id is not None else None,
            reference_date=reference_date if reference_date is not None else None,
            reference_link=reference_link if reference_link is not None else None,
            title=title if title is not None else title,
            content=content if content is not None else None,
            thumbnail=thumbnail if thumbnail is not None else None,
        )

    def __iter__(self):
        for k, v in self.to_dict().items():
            yield k, v
