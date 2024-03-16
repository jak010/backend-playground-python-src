from __future__ import annotations

from abc import ABCMeta
from typing import Generic, TypeVar

from dependency_injector.wiring import Provide
from sqlalchemy.orm import Session

from src.domain.posts.post_entity import PostEntity
from settings.dependency import DataBaseContainer

Entity = TypeVar("Entity")


class IRepository(Generic[Entity], metaclass=ABCMeta):
    session: Session = Provide[DataBaseContainer.session]


class PostRepository(IRepository[PostEntity]):

    def save(self, post_entity: PostEntity):
        self.session.add(post_entity)
        self.session.flush()
        self.session.commit()

    def find_by_pk(self, pk: int) -> PostEntity:
        query = self.session.query(PostEntity).filter(PostEntity.pk == pk)
        return query.one_or_none()
