from __future__ import annotations

import datetime
import json
from abc import ABCMeta

import nanoid as _nanoid


class AbstractEntity(metaclass=ABCMeta):
    pk: int
    nanoid: str

    created_at: datetime.datetime
    modified_at: datetime.datetime

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def new(cls, *args, **kwargs) -> AbstractEntity:
        ...

    def to_dict(self):
        data = {}
        for k, v in self.__dict__.items():
            if isinstance(v, int):
                data[k] = int(v)
            if isinstance(v, str):
                data[k] = str(v)
            if isinstance(v, datetime.datetime):
                data[k] = v.isoformat()
            else:
                data[k] = data

    @staticmethod
    def generate_nano_id() -> str:
        return _nanoid.generate(size=24)

    def __repr__(self):
        items = {}

        for k, v in self.__dict__.items():
            if not k.startswith('_'):

                if isinstance(type(v), datetime.datetime):
                    items[k] = v.isoformat
                if isinstance(v, bool):
                    items[k] = str(v)
                else:
                    items[k] = str(v)

        return f"{self.__class__.__name__}({json.dumps(items, ensure_ascii=False, indent=4)})"
