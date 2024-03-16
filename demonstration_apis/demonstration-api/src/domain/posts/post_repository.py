from __future__ import annotations

from abc import ABCMeta
from typing import Generic, TypeVar

from dependency_injector.wiring import Provide
from sqlalchemy.orm import Session

from src.domain.posts.post_entity import PostEntity, LikeIncreateLimitException
from settings.dependency import DataBaseContainer

Entity = TypeVar("Entity")


class IRepository(Generic[Entity], metaclass=ABCMeta):
    session: Session = Provide[DataBaseContainer.session]


class PostRepository(IRepository[PostEntity]):

    def save(self, post_entity: PostEntity):
        self.session.add(post_entity)
        self.session.commit()
        self.session.close()

    def find_by_pk(self, pk: int) -> PostEntity:
        query = self.session.query(PostEntity).filter(PostEntity.pk == pk).one()
        self.session.commit()
        self.session.close()
        return query

    def increase_like(self, pk: int) -> PostEntity:
        query = self.session.query(PostEntity).filter(PostEntity.pk == pk).one()
        query.like += 1

        if query.like > 500:
            self.session.rollback()
            raise LikeIncreateLimitException()

        self.session.add(query)
        self.session.commit()
        self.session.close()