import random
import uuid

import nanoid

from usages.sqlalchemy_imperative_mapping_style.config.client import get_engine
from usages.sqlalchemy_imperative_mapping_style.config.sa_models import Member
from usages.sqlalchemy_imperative_mapping_style.config.start_mappers import start_mapper

# from sqlalchemy.orm.session import Session

INSERT_DATA_COUNT = 1_000_000


def list_setup():
    return [Member(
        nanoid=nanoid.generate(size=24),
        name=uuid.uuid4().hex[:5],
        age=random.randint(1, 100),
        address1=uuid.uuid4().hex[:5],
        address2=uuid.uuid4().hex[:5],
    ) for _ in range(INSERT_DATA_COUNT)]


def generate_setup():
    for _ in range(INSERT_DATA_COUNT):
        yield {
            "nanoid": nanoid.generate(size=24),
            "name": uuid.uuid4().hex[: 5],
            "age": random.randint(1, 100),
            "address1": uuid.uuid4().hex[: 5],
            "address2": uuid.uuid4().hex[: 5]
        }


def get_member(engine):
    start_time = time.time()

    r = list_setup()

    print(time.time() - start_time)
    return r


if __name__ == '__main__':
    import time

    start_time = time.time()
    engine = get_engine()

    start_mapper()

    get_member(engine)

    engine.dispose()
    print(time.time() - start_time)
