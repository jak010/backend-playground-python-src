import copy
import dataclasses
import json

from src.adapter.voguekorea.api.libs.dto import VogueKoreaDto
from src.libs.resource.common.define import CONVERT
from src.libs.resource.common.universal_entity import UniversalEntity
from src.libs.resource.voguekorea.voguekorea_service import VogueKoreaService


@dataclasses.dataclass
class VogueKoreaEntity(UniversalEntity):

    def __repr__(self):
        _content = copy.deepcopy(self.content)

        _repr = self.__class__.__name__ + "("
        _repr += json.dumps({
            "id": self.id,
            "trace_id": self.trace_id,
            "is_convert": self.is_convert,
            "reference_id": self.reference_id,
            "reference_date": self.reference_date.isoformat(),
            "reference_link": self.reference_link,
            "title": self.title,
            "content": _content[0:7] + f"...({len(_content)}size)",
            "thumbnail": self.thumbnail
        }, ensure_ascii=False, indent=4)
        _repr += ")"
        return _repr

    @classmethod
    def from_dto(cls, voguekorea_dto: VogueKoreaDto):
        return cls(
            id=None,
            trace_id=voguekorea_dto.trace_id,
            reference_id=voguekorea_dto.reference_id,
            reference_date=VogueKoreaService.to_datetime(voguekorea_dto.reference_date),
            reference_link=voguekorea_dto.reference_link,
            thumbnail=voguekorea_dto.thumbnail,
            is_convert=CONVERT.OFF.value,
            title=voguekorea_dto.title,
            content=voguekorea_dto.content
        )
