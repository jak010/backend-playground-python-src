from dependency_injector.wiring import Provide
from config.container import SqlAlchemyConatiner
from sqlalchemy.orm import Session

from typing import Generic, TypeVar, get_args, Type

T = TypeVar("T")


class ISqlalchemyRepository:
    session: Session = Provide[SqlAlchemyConatiner.session]

    def save(self, model):
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        self.session.commit()
        return model

    def delete(self, user_id: int): ...

    def find_by_id(self, user_id: int): ...


class ISqlalchemyRepositoryV2(Generic[T]):
    session: Session = Provide[SqlAlchemyConatiner.session]

    def save(self, model):
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        self.session.commit()
        return model

    def delete_by_id(self, pk: int):
        model = self.__get_model()
        query = self.session.query(model).filter(model.id == pk).one_or_none()
        if query:
            return query.delete()
        raise Exception("Not Exist Entity Error")

    def find_by_id(self, pk: int):
        model = self.__get_model()

        query = self.session.query(model).filter(model.id == pk).one_or_none()
        if query:
            return query
        raise Exception("Not Exist Entity Error")

    def __get_model(self):  # NOTE, 241130 : Generic "T" inference
        return self.__orig_bases__[0].__args__[0]
