from __future__ import annotations

import time

from src.domain.abstract import AbstractEntity


class LikeIncreateLimitException(Exception):
    """ Like 최대 증가 개수 제한 """


class PostEntity(AbstractEntity):
    like: int
    version: int
    modified_at: int

    @classmethod
    def new(cls, like: int, version: int, modified_at: int):
        return cls(
            like=like,
            version=version,
            modified_at=modified_at
        )

    def increase_like(self):
        if self.like >= 1000:
            raise LikeIncreateLimitException()

        self.like += 1
        self.modified_at = time.time()

    def reset_like(self):
        self.like = 0
