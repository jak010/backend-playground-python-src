import dataclasses
import ipaddress
import time
from typing import Optional

from fastapi import Request


@dataclasses.dataclass
class PostHistoryEntity:
    id: Optional[int]
    post_id: Optional[int]

    ip: int
    port: int
    referrer: str
    useragent: str
    created_at: int

    def to_dict(self):
        return dataclasses.asdict(self)

    @classmethod
    def new(cls, post_id, request: Request):
        return cls(
            post_id=post_id,
            ip=int(ipaddress.ip_address(request.client.host)),
            port=int(request.client.port),
            referrer=request.headers.get('referer', ""),
            useragent=request.headers.get("user-agent", ""),
            created_at=int(time.time()),
            id=None
        )
