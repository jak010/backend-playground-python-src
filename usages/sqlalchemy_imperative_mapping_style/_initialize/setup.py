import random

from usages.sqlalchemy_imperative_mapping_style.config.sa_models import Member
from usages.sqlalchemy_imperative_mapping_style.config.start_mappers import start_mapper

from usages.sqlalchemy_imperative_mapping_style.config.client import get_session, get_engine
import nanoid
import uuid

INSERT_DATA_COUNT = 1_000_000


def get_member(e):
    s = get_session(e)

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
            s.bulk_save_objects(grouping)
            grouping.clear()
            print(f'inserted: {x}')

    if grouping:
        s.bulk_save_objects(grouping)
        print(f'inserted: {x}')

    s.commit()
    s.close()


if __name__ == '__main__':
    engine = get_engine()

    start_mapper()

    get_member(engine)

    engine.dispose()
