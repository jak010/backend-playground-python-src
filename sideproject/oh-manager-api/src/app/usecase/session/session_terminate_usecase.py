from src.app.domain.session import SessionEntity
from src.app.usecase.abstract import AbstractUseCase


class SessionTerminateUseCase(AbstractUseCase):

    @classmethod
    def execute(cls, session: SessionEntity):
        cls.session_repository.delete(session_entity=session)
