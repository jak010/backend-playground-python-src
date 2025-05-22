import sys
import time
import os
import random
import uuid

from usages.database_usecase.config.sa_models import Member

import nanoid

# from dataclasses import dataclass, asdict
# @dataclass
# class Member:
#     nanoid: str
#     name: str
#     age: int
#     address1: str
#     address2: str
#
#
#     def to_dict(self):
#         return asdict(self)
#

MILLION = 1_000_000


def get_random_with_urandom():
    return os.urandom(16).hex()  # 16바이트 = 128비트


def get_random_with_uuid():
    return uuid.uuid4().hex


def generate_member_object():
    start_time = time.time()

    grouping = [Member(
        nanoid=nanoid.generate(size=12),
        name=get_random_with_urandom(),
        age=random.randint(1, 100),
        address1=get_random_with_urandom(),
        address2=get_random_with_urandom()
    ) for _ in range(MILLION)]

    print("MEMBER OBJECT SPENT TIME", time.time() - start_time)

    return grouping
