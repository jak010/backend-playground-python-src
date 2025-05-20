import os
import random
import time

from usages.sqlalchemy_imperative_mapping_style.config.client import get_session, get_engine
from usages.sqlalchemy_imperative_mapping_style.config.sa_models import Member
from usages.sqlalchemy_imperative_mapping_style.config.start_mappers import start_mapper

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

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


def worker(data):
    engine = get_engine()

    start_mapper()

    _session = get_session(engine)
    _session.bulk_save_objects(data)
    _session.commit()
    _session.close()

    engine.dispose()


def write_thread_member(data):
    import time
    start_time = time.time()
    CHUNK_SIZE = 500

    futures = []
    worker_process = os.cpu_count() * 2 + 1
    with ProcessPoolExecutor(max_workers=worker_process) as executor:
        for i in range(0, len(data), CHUNK_SIZE):
            chunk = data[i:i + CHUNK_SIZE]
            future = executor.submit(worker, chunk)
            futures.append(future)

        # 반드시 결과를 기다려야 함!
        for future in futures:
            future.result()  # 예외도 여기서 catch됨

    print(time.time() - start_time)


if __name__ == '__main__':
    write_thread_member(data=generate_member_object())
