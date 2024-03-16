from __future__ import annotations

from src.domain.abstract import AbstractEntity


class LikeIncreateLimitException(Exception):
    """ Like 최대 증가 개수 제한 """


class PostEntity(AbstractEntity):
    like: int

    @classmethod
    def new(cls, like: int):
        return cls(

            like=like
        )

    def increase_like(self):
        if self.like >= 500:
            raise LikeIncreateLimitException()

        self.like += 1

    def reset_like(self):
        self.like = 0
