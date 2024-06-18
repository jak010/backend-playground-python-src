from __future__ import annotations

import dataclasses
import time
from functools import cached_property


@dataclasses.dataclass(frozen=True)
class KaKaoAccessTokenInfoDto:
    id: int  # 회원번호
    expires_in: int  # 액세스 토큰 만료시간(초)
    app_id: int

    # depreacated property
    appId: int = dataclasses.field(default=0)
    expiresInMillis: int = dataclasses.field(default=0)

    """
    {
        "expiresInMillis": 21296647,
        "id": 1234,
        "expires_in": 21296,
        "app_id": 1045160,
        "appId": 1045160
    }
    """

    @cached_property
    def expires_in_timestamp(self) -> int:
        return int(time.time()) + self.expires_in
