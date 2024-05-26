from functools import wraps

# from external_library.database import SQLAlchemyConnector

from library.abstract import AbstractRdbRepsitory
from src.member.exceptions import MemberNotFound


def Transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = AbstractRdbRepsitory.session

        try:
            print("Transactionl", session)
            f = func(*args, **kwargs)
            print(f)
            session.commit()
            session.remove()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        return f

    return wrapper
