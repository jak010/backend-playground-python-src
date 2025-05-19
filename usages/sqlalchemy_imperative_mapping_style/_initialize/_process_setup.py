import os, random, uuid, time
from concurrent.futures import ProcessPoolExecutor
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, text
import nanoid
from usages.sqlalchemy_imperative_mapping_style.config.client import get_session

INSERT_DATA_COUNT = 1_000_000
BATCH_SIZE = 5000
MAX_WORKERS = min(os.cpu_count(), 8)


def get_engine():
    return create_engine(
        URL.create(
            drivername="mysql+pymysql",
            username='root',
            password="1234",
            database="demo",
            host="127.0.0.1",
            port=19501
        ),
        pool_pre_ping=True,
        future=True
    )


def generate_member_dict():
    for _ in range(INSERT_DATA_COUNT):
        yield {
            "nanoid": nanoid.generate(size=24),
            "name": uuid.uuid4().hex[:5],
            "age": random.randint(1, 100),
            "address1": uuid.uuid4().hex,
            "address2": uuid.uuid4().hex,
        }


def create_batches():
    batch = []
    for row in generate_member_dict():
        batch.append(row)
        if len(batch) >= BATCH_SIZE:
            yield batch
            batch = []
    if batch:
        yield batch


def worker(batch):
    engine = get_engine()
    session = get_session(engine)
    print(f'Process {os.getpid()} inserting {len(batch)} rows...')
    session.execute(
        text("""
            INSERT INTO member (nanoid, name, age, address1, address2)
            VALUES (:nanoid, :name, :age, :address1, :address2)
        """), batch
    )
    session.commit()
    session.close()
    engine.dispose()


if __name__ == '__main__':
    start_time = time.time()

    batches = list(create_batches())

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        list(executor.map(worker, batches))

    print(f'Total time: {time.time() - start_time:.2f} seconds')
