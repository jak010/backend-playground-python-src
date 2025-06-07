""" Pessimistic Lock, 비관적 락
    비관적 락이 적용되지 않은 경우를 어떻게 동작하는 관찰하기

    Notice:

"""
import threading
import time

from usages.database_usecase._initialize.imperative_mapped_setup import start_mapper
from usages.database_usecase.config.client import get_session, get_engine
from usages.database_usecase.excercieses.imperative_mapping_style.entities import MemberEntity


def worker1(engine):
    s = get_session(engine)
    r = s.query(MemberEntity).filter(MemberEntity.nanoid == 'U3M065V1XtRa').one_or_none()
    time.sleep(0.1)
    r.age += 1
    print("[Worker1] Member Age:", r.age)
    s.commit()
    s.close()


def worker2(engine):
    s = get_session(engine)
    r = s.query(MemberEntity).filter(MemberEntity.nanoid == 'U3M065V1XtRa').one_or_none()
    time.sleep(0.1)
    r.age -= 1
    print("[Worker2] Member Age:", r.age)
    s.commit()
    s.close()


if __name__ == '__main__':
    start_mapper(lazy_option="raise")

    engine = get_engine()

    ths = []
    for _ in range(25):
        th1 = threading.Thread(target=worker1, args=(engine,))
        ths.append(th1)
        th2 = threading.Thread(target=worker2, args=(engine,))
        ths.append(th2)

    for th in ths:
        th.start()

    for th in ths:
        th.join()

    engine.dispose()
