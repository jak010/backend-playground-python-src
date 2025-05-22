import time
import threading

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

    ths = []

    chunk_size = 10_000
    for i in range(0, len(members), chunk_size):
        member_chnuk = members[i:i + chunk_size]
        th = threading.Thread(target=save_member, args=(engine, member_chnuk))
        ths.append(th)
        th.start()

    for th in ths:
        th.join()

    print(time.time() - start_time)

    engine.dispose()


if __name__ == '__main__':
    insert_member()
