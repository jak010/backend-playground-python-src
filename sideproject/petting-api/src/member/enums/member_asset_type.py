from enum import Enum, unique


@unique
class MemberAssetType(Enum):
    COIN = 'COIN'

    @classmethod
    def to(cls, value: str):
        if value == cls.COIN.value:
            return cls.COIN
