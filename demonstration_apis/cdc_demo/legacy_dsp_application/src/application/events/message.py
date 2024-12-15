import json
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class DomainMessage:
    aggregate_id: int
    aggregate_type: str
    occured_on: str
    owner_id: int

    @classmethod
    def of(cls, aggregate_id: int, aggregate_type: str, occred_on: str, owner_id: int):
        return cls(
            aggregate_id=aggregate_id,
            aggregate_type=aggregate_type,
            occured_on=occred_on,
            owner_id=owner_id
        )

    def to_output_message(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")
