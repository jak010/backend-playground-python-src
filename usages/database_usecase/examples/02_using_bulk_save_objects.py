import time

from usages.database_usecase._initialize.notepad import generate_member_object
from usages.database_usecase.config.client import get_session, get_engine


def save_member(engine, members):
    s = get_session(engine)

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
    insert_member()
