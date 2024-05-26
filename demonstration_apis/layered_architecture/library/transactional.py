from functools import wraps

# from external_library.database import SQLAlchemyConnector

from library.abstract import AbstractRdbRepsitory
from src.member.service.exceptions import ServiceException


def Transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = AbstractRdbRepsitory.get_session()

        try:
            print("Transactionl", session)
            f = func(*args, **kwargs)


        except ServiceException as e:
            print(e.args)
            session.rollback()
            raise e
        finally:
            session.commit()
            session.remove()
            session.close()

        return f

    return wrapper
