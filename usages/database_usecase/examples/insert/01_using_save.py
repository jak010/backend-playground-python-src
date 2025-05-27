import time
from usages.database_usecase.config.sa_models import Member
from usages.database_usecase.config.start_mappers import start_mapper

from usages.database_usecase.config.client import get_session, get_engine

from usages.database_usecase._initialize.notepad import generate_member_object

from sqlalchemy import text


def save_member(engine, members):
    s = get_session(engine)

    for member in members:
        s.add(member)

    s.bulk_save_objects(members)

    s.commit()
    s.close()


def insert_member():
    engine = get_engine()

    members = generate_member_object()

    start_time = time.time()
    save_member(engine, members)

    print(time.time() - start_time)

    engine.dispose()


if __name__ == '__main__':
    start_mapper()

    insert_member()
