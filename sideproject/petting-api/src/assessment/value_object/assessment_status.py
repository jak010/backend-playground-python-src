from enum import Enum, unique


@unique
class AssessmentStatus(Enum):
    WAIT = "WAIT"
    REJECT = "REJECT"
    APPROVE = "APPROVE"

    @classmethod
    def to(cls, value: str):
        if value == cls.WAIT.value:
            return cls.WAIT
        if value == cls.REJECT.value:
            return cls.REJECT
        if value == cls.APPROVE.value:
            return cls.APPROVE
