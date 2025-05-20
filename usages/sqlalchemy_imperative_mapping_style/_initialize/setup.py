import os
import random
import time

from usages.sqlalchemy_imperative_mapping_style.config.client import get_session, get_engine
from usages.sqlalchemy_imperative_mapping_style.config.sa_models import Member
from usages.sqlalchemy_imperative_mapping_style.config.start_mappers import start_mapper

INSERT_DATA_COUNT = 1_000_000


def get_random_with_urandom():
    return os.urandom(16).hex()  # 16바이트 = 128비트


def generate_member_object():
    start_time = time.time()

    grouping = []
    for x in range(INSERT_DATA_COUNT):
        _new_nanoid = get_random_with_urandom()[0:3]
        _new_name = get_random_with_urandom()[0:3]
        _new_age = random.randint(1, 100)
        _address1 = get_random_with_urandom()[0:10]
        _address2 = get_random_with_urandom()[0:10]
        grouping.append(Member(
            nanoid=_new_nanoid,
            name=_new_name,
            age=_new_age,
            address1=_address1,
            address2=_address2
        ))

    print("MEMBER OBJECT SPENT TIME", time.time() - start_time)

    return grouping


def write_member(engine):
    members = generate_member_object()
    start_time = time.time()

    _session = get_session(engine)
    _session.bulk_insert_mappings(Member, [{
        'nanoid': member.nanoid,
        'name': member.name,
        'age': member.age,
        'address1': member.address1,
        'address2': member.address2
    } for member in members])
    _session.commit()
    _session.close()

    print("DB INSERT SPENT TIME", time.time() - start_time)


if __name__ == '__main__':
    engine = get_engine()

    start_mapper()

    write_member(engine)

    engine.dispose()
