import random

from usages.sqlalchemy_imperative_mapping_style.config.sa_models import Member
from usages.sqlalchemy_imperative_mapping_style.config.start_mappers import start_mapper

from usages.sqlalchemy_imperative_mapping_style.config.client import get_session, get_engine
# from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine
import threading
import nanoid
import uuid
import os

INSERT_DATA_COUNT = 1_000_000

lock = threading.Lock()

count = 0


def worker(engine: Engine, data):
    global count
    print(f'inserted: {len(data)}')
    count += len(data)
    print(os.getpid(), threading.get_ident())
    _session = get_session(engine)

    _session.bulk_save_objects(data)

    _session.commit()
    _session.close()


threads = []


def get_member(e):
    grouping = []

    for x in range(INSERT_DATA_COUNT):
        _new_nanoid = nanoid.generate(size=24)
        _new_name = str(uuid.uuid4().hex[0:5])
        _new_age = random.randint(1, 100)
        _address1 = uuid.uuid4().hex
        _address2 = uuid.uuid4().hex

        grouping.append(Member(
            nanoid=_new_nanoid,
            name=_new_name,
            age=_new_age,
            address1=_address1,
            address2=_address2
        ))

        if len(grouping) >= 500:
            th = threading.Thread(target=worker, kwargs={"engine": e, "data": grouping.copy()})
            th.start()
            threads.append(th)
            grouping.clear()


if __name__ == '__main__':
    import time

    start_time = time.time()
    engine = get_engine()

    start_mapper()

    get_member(engine)

    for th in threads:
        th.join()

    engine.dispose()
    print(count)
    print(time.time() - start_time)
