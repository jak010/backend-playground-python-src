from __future__ import annotations

from typing import TypeVar, Generic

from pydantic import BaseModel

from src.app.controller.swagger.util import entity_to_outputmodel
from src.app.domain.auditions.audition_entity import AuditionEntity

PYDANTIC_BASE_MODEL = TypeVar('PYDANTIC_BASE_MODEL', bound=BaseModel)


class ResponseEntityModel(BaseModel, Generic[PYDANTIC_BASE_MODEL]):
    items: list[PYDANTIC_BASE_MODEL]


AUDITIONS_ENTITY_MODEL = entity_to_outputmodel(
    AuditionEntity,
    name='AuditionEntityOutModel',
    exclude_fields=[
        "uid",
        "author",
        "platform",
        "link",
        "created_at",
        "modified_at"
    ]
)
