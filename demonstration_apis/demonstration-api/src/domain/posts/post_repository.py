from __future__ import annotations
import backoff
import time
from abc import ABCMeta
from typing import Generic, TypeVar

from dependency_injector.wiring import Provide, Closing
from sqlalchemy.orm import Session

from src.domain.posts.post_entity import PostEntity, LikeIncreateLimitException
from settings.dependency import DataBaseContainer
from settings.abstracts import IRepository

Entity = TypeVar("Entity")


class OptimisticLockFail(Exception):
    """ Optimistic Lock이 실패한다. """


class PostRepository(IRepository[PostEntity]):

    def find_by_id(self) -> PostEntity:
        ...

    def find_by_pk(self, pk: int) -> PostEntity:
        """ without lock """
        query = self.session.query(PostEntity).filter(PostEntity.pk == pk).one()
        return query

    def find_by_pk_by_pessimisitic_lock(self, pk: int) -> PostEntity:
        """ pessimisitic lock """
        query = self.session.query(PostEntity).filter(PostEntity.pk == pk).with_for_update().one()
        return query

    def increase_like(self, post_entity: PostEntity) -> PostEntity:
        if post_entity.like >= 1000:
            raise LikeIncreateLimitException()

        self.session.query(PostEntity).filter(PostEntity.pk == post_entity.pk) \
            .update(
            {
                PostEntity.like: post_entity.like + 1,
                PostEntity.modified_at: int(time.time())
            }
        )
        self.session.commit()
        self.session.close()

    @backoff.on_exception(backoff.expo, OptimisticLockFail, max_tries=3)
    def increase_like_by_optimistic_lock(self, post_entity: PostEntity):
        if post_entity.like >= 1000:
            raise LikeIncreateLimitException()

        result = self.session.query(PostEntity).filter(
            PostEntity.pk == post_entity.pk,
            PostEntity.version == post_entity.version
        ).update({
            PostEntity.like: post_entity.like + 1,
            PostEntity.modified_at: int(time.time()),
            PostEntity.version: post_entity.version + 1
        })

        if not bool(result):
            raise OptimisticLockFail()

        self.session.commit()
        self.session.close()
        return result

    def increase_like_by_optimistic_lock_in_mapper_args(self, post_entity: PostEntity):
        """
            Path: backend-playground-src/demonstration_apis/demonstration-api/src/utils.py
            Ref: https://docs.sqlalchemy.org/en/20/orm/versioning.html#simple-version-counting
        """
        if post_entity.like >= 1000:
            raise LikeIncreateLimitException()

        post_entity.increase_like()
        self.session.add(post_entity)

        self.session.commit()
        self.session.close()
        # return result
