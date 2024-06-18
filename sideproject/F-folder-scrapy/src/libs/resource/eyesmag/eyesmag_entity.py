import copy
import dataclasses
import json

from src.adapter.eyesmag.api.libs.dto import EyesMagDto
from src.libs.resource.common.define import CONVERT
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.eyesmag.eyesmag_service import EyesMagService


@dataclasses.dataclass
class EyesMagEntity(UniversalEntity):

    def __repr__(self):
        _content = copy.deepcopy(self.content)

        _repr = self.__class__.__name__ + "("
        _repr += json.dumps({
            "id": self.id,
            "trace_id": self.trace_id,
            "reference_id": self.reference_id,
            "reference_date": self.reference_date.isoformat(),
            "reference_link": self.reference_link,
            "is_convert": self.is_convert,
            "title": self.title,
            "content": _content[0:5] + f"...({len(_content)}size)",
            "thumbnail": self.thumbnail
        }, ensure_ascii=False, indent=4)
        _repr += ")"
        return _repr

    @classmethod
    def from_dto(cls, eyesmag_dto: EyesMagDto):
        return cls(
            id=None,
            trace_id=eyesmag_dto.trace_id,
            reference_id=eyesmag_dto.reference_id,
            reference_date=EyesMagService.to_datetime(eyesmag_dto.reference_date),
            reference_link=eyesmag_dto.reference_link,
            thumbnail=eyesmag_dto.thumbnail,
            is_convert=CONVERT.OFF.value,
            title=eyesmag_dto.title,
            content=eyesmag_dto.content
        )
