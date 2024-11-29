from dependency_injector.wiring import Provide
from config.container import SqlAlchemyConatiner
from sqlalchemy.orm import Session


class ISqlalchemyRepository:
    session: Session = Provide[SqlAlchemyConatiner.session]

    def save(self, model): ...

    def delete(self, user_id: int): ...

    def find_by_id(self, user_id: int): ...
