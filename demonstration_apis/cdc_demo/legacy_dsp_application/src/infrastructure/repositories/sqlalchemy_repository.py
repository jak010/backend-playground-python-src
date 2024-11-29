from dependency_injector.wiring import Provide
from config.container import SqlAlchemyConatiner
from sqlalchemy.orm import Session


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
