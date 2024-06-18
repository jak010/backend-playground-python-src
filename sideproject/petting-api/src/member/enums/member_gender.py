from enum import Enum, unique


@unique
class MemberGender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'

    @classmethod
    def to_obj(cls, gender: str):
        if gender == MemberGender.MALE.value:
            return cls.MALE
        if gender == MemberGender.FEMALE.value:
            return cls.FEMALE
