import copy
import dataclasses
import json
import time
import uuid
from typing import Optional, Union, Any


@dataclasses.dataclass
class PostEntity:
    title: str = dataclasses.field(init=True)
    keyword: Optional[str] = dataclasses.field(init=True)
    content: Union[Optional[str], Any] = dataclasses.field(init=True)
    reference_link: str = dataclasses.field(init=True)

    trace_id: str | uuid.UUID = dataclasses.field(init=True)
    platform: str = dataclasses.field(init=True)

    thumbnail: str
    created_at: int
    modified_at: int
    is_temporary: int
    is_deleted: int
    views: int
    post_id: Optional[int]

    def to_dict(self):
        return dataclasses.asdict(self)

    @classmethod
    def new(cls,
            *,
            title: str,
            content: str,
            keyword: str,
            trace_id: uuid.UUID,
            platform: str,
            reference_link: str,
            thumbnail: str,
            created_at: int
            ):
        return cls(
            post_id=None,
            trace_id=trace_id,
            reference_link=reference_link,
            thumbnail=thumbnail,
            title=title,
            content=content,
            keyword=keyword,
            platform=platform,
            is_temporary=0,
            is_deleted=0,
            views=0,
            created_at=created_at,
            modified_at=int(time.time())
        )

    def __repr__(self):
        _content = copy.deepcopy(self.content)

        _repr = self.__class__.__name__ + "("
        _repr += json.dumps({
            "id": self.post_id,
            "trace_id": self.trace_id,
            "reference_link": self.reference_link,
            "title": self.title,
            "content": _content[0:7] + f"...({len(_content)}size)",
            "keyword": self.keyword,
            "platform": self.platform,
            "is_temporary": self.is_temporary,
            "is_deleted": self.is_deleted,
            "views": self.views,
            "created_at": self.created_at,
            "modified_at": self.modified_at
        }, ensure_ascii=False, indent=4)
        _repr += ")"
        return _repr
