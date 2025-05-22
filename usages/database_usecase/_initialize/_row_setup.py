import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

import MySQLdb
from dbutils.pooled_db import PooledDB

INSERT_DATA_COUNT = 1_000_000
CHUNK_SIZE = 20_000
MAX_WORKERS = os.cpu_count() * 2 + 1

# 1. Connection Pool 구성
pool = PooledDB(
    creator=MySQLdb,  # 사용할 DB API 모듈
    maxconnections=MAX_WORKERS + 5,  # 최대 커넥션 수
    mincached=4,  # 시작 시 생성할 커넥션 수
    maxcached=10,  # 캐시에 유지할 최대 커넥션 수
    blocking=False,
    host="127.0.0.1",
    port=19501,
    user="root",
    passwd="1234",
    db="demo",
    charset="utf8"
)


def get_random_with_urandom():
    return os.urandom(16).hex()


def generate_member_object():
    start_time = time.time()
    grouping = []
    for _ in range(INSERT_DATA_COUNT):
        grouping.append({
            'nanoid': get_random_with_urandom()[:3],
            'name': get_random_with_urandom()[:3],
            'age': random.randint(1, 100),
            'address1': get_random_with_urandom()[:10],
            'address2': get_random_with_urandom()[:10]
        })
    print(time.time() - start_time)
    return grouping


def worker(chunk):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO member (nanoid, name, age, address1, address2) VALUES (%(nanoid)s, %(name)s, %(age)s, %(address1)s, %(address2)s)",
        chunk
    )
    conn.commit()
    cursor.close()
    conn.close()


def main():
    members = generate_member_object()

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i in range(0, len(members), CHUNK_SIZE):
            chunk = members[i:i + CHUNK_SIZE]
            executor.submit(worker, chunk)
    print(f"Inserted {len(members)} records in {time.time() - start_time:.2f} seconds")


if __name__ == '__main__':
    main()
