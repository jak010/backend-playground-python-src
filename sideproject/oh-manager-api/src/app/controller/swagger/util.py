from __future__ import annotations

from typing import get_type_hints, Type, TypeVar, Generic

from pydantic import BaseModel, create_model, Field

from src.app.domain.abstract import AbstractDomainEntity

PYDANTIC_BASE_MODEL = TypeVar('PYDANTIC_BASE_MODEL', bound=BaseModel)


class ResponseModel(BaseModel, Generic[PYDANTIC_BASE_MODEL]):
    items: list[PYDANTIC_BASE_MODEL]


def entity_to_outputmodel(entity: AbstractDomainEntity, name: str, exclude_fields: list) -> Type[BaseModel]:
    """Converts a stdlib dataclass to a pydantic BaseModel"""
    attributes = {}
    for k, v in get_type_hints(entity).items():
        if k in exclude_fields:
            attributes[k] = (v, Field(..., exclude=True))
        else:
            attributes[k] = (v, Field(..., include=True))
    return create_model(name, **attributes)
