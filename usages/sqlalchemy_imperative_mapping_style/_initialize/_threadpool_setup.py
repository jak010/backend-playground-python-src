import os
import random
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

import nanoid
# from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine

from usages.sqlalchemy_imperative_mapping_style.config.client import get_session, get_engine
from usages.sqlalchemy_imperative_mapping_style.config.sa_models import Member
from usages.sqlalchemy_imperative_mapping_style.config.start_mappers import start_mapper
import pandas as pd

INSERT_DATA_COUNT = 1_000_000

from functools import lru_cache


def worker(engine, data):
    print(f'inserted: {len(data)}')

    # ORM
    _session = get_session(engine)
    print(os.getpid(), threading.get_ident())

    _session.bulk_insert_mappings(Member, [{
        'nanoid': m.nanoid,
        'name': m.name,
        'age': m.age,
        'address1': m.address1,
        'address2': m.address2
    } for m in data])

    _session.commit()
    _session.close()


threads = []


def generate_member():
    for _ in range(INSERT_DATA_COUNT):
        yield Member(
            nanoid=nanoid.generate(size=24),
            name=str(uuid.uuid4().hex[0:5]),
            age=random.randint(1, 100),
            address1=uuid.uuid4().hex,
            address2=uuid.uuid4().hex
        )


def get_member(engine, exe):
    grouping = []
    futures = []

    count = 0
    for member in generate_member():
        count += 1
        grouping.append(member)

        if count >= 500:
            count = 0
            futures.append(exe.submit(worker, engine, grouping.copy()))
            grouping.clear()

    return futures


if __name__ == '__main__':
    import time

    start_time = time.time()
    engine = get_engine()

    start_mapper()

    max_workers = os.cpu_count() * 2 + 1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = get_member(engine, executor)

        for f in as_completed(futures):
            f.result()

    engine.dispose()
    print(time.time() - start_time)
