""" Pessimistic Lock, 비관적 락

    비관적 락이 적용되지 않은 경우를 어떻게 동작하는 관찰하기

    Member.Age가 0에서 출발해 Member.age +=1 과 Member.age -= 1이 번갈아 실행되기 때문에 결과는 Member.Age는 항상 0이 되어야한다.
    그러나 Pessimistic Lock이 적용되지 않는 코드는 이러한 정합성을 보장하지 않는다.

    Notice:
        pessmistic lock 쿼리에 "select ..for update"를 적용함으로써 효과를 볼 수 있다.
        pessmistic lock이 적용되지 않은 쿼리는 Member Age이 결과가 항상 0이 아니지만 pessmistic lock은 정합성을 보장하기 떄문에 항상 0이 된다.

"""
import threading
import time

from usages.database_usecase._initialize.imperative_mapped_setup import start_mapper
from usages.database_usecase.config.client import get_session, get_engine
from usages.database_usecase.excercieses.imperative_mapping_style.entities import MemberEntity


def worker1(engine):
    s = get_session(engine)
    r = s.query(MemberEntity) \
        .filter(MemberEntity.nanoid == 'U3M065V1XtRa') \
        .with_for_update() \
        .one_or_none()  # pessmistic lock
    time.sleep(0.1)
    r.age += 1
    print("[Worker1] Member Age:", r.age)
    s.commit()
    s.close()


def worker2(engine):
    s = get_session(engine)
    r = s.query(MemberEntity)\
        .filter(MemberEntity.nanoid == 'U3M065V1XtRa')\
        .with_for_update()\
        .one_or_none()  # pessmistic lock
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
