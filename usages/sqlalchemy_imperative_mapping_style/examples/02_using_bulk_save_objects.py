import time

from usages.sqlalchemy_imperative_mapping_style._initialize.notepad import generate_member_object
from usages.sqlalchemy_imperative_mapping_style.config.client import get_session, get_engine
from usages.sqlalchemy_imperative_mapping_style.config.start_mappers import start_mapper


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
    start_mapper()

    insert_member()
