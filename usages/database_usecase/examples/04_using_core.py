import time

from usages.database_usecase._initialize.notepad import generate_member_object
from usages.database_usecase.config.client import get_session, get_engine
from usages.database_usecase.config.sa_models import Member
from usages.database_usecase.config.start_mappers import start_mapper


def insert_member():
    engine = get_engine()

    members = generate_member_object()

    start_time = time.time()

    engine.execute(
        Member.__table__.insert(),
        [
            {
                'nanoid': member.nanoid,
                'name': member.name,
                'age': member.age,
                'address1': member.address1,
                'address2': member.address2
            } for member in members
        ]
    )

    print(time.time() - start_time)

    engine.dispose()


if __name__ == '__main__':
    start_mapper()

    insert_member()
