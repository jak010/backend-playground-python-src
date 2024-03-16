from __future__ import annotations

import time

from src.domain.abstract import AbstractEntity


class LikeIncreateLimitException(Exception):
    """ Like 최대 증가 개수 제한 """


class PostCommentEntity(AbstractEntity):
    post_id: int
    created_at: int

    @classmethod
    def new(cls, post_id: int, create_at: int):
        return cls(
            post_id=post_id,
            create_at=create_at
        )
