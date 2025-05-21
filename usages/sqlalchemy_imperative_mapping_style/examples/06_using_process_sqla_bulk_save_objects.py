import time
from multiprocessing import Process

from usages.sqlalchemy_imperative_mapping_style._initialize.notepad import generate_member_object
from usages.sqlalchemy_imperative_mapping_style.config.client import get_session, get_engine
from usages.sqlalchemy_imperative_mapping_style.config.start_mappers import start_mapper

from usages.sqlalchemy_imperative_mapping_style.config.sa_models import Member


def save_member(members):
    # 프로세스 내부에서 engine 생성
    engine = get_engine()
    s = get_session(engine)

    s.bulk_insert_mappings(Member, members)
    s.commit()
    s.close()

    engine.dispose()


def generate_member_dict(members):
    return [
        {
            'nanoid': member.nanoid,
            'name': member.name,
            'age': member.age,
            'address1': member.address1,
            'address2': member.address2
        } for member in members
    ]


def insert_member():
    members = generate_member_object()
    chunk_size = 10_000

    start_time = time.time()

    processes = []

    for i in range(0, len(members), chunk_size):
        member_dict = generate_member_dict(members[i:i + chunk_size])
        p = Process(target=save_member, args=(member_dict,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("Time taken:", time.time() - start_time)


if __name__ == '__main__':
    insert_member()
