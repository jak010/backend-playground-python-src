from __future__ import annotations

import logging

from dependency_injector.wiring import Provide
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.orm import Session

from src.config.container.context import ContextContainer

logger = logging.getLogger("Session")
logger.setLevel(level=0)


class Transactional:
    session: Session = Provide[ContextContainer.session]

    # @cached_property
    # @inject
    # def _session(self, session=Provide[ContextContainer.session]):
    #     return session

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self.session.begin():
                try:
                    result = func(*args, **kwargs)
                    self.session.commit()
                    return result
                except OperationalError as e:
                    self.session.rollback()
                    self.session.close()
                except IntegrityError as e:
                    self.session.rollback()
                    self.session.close()

        return wrapper
