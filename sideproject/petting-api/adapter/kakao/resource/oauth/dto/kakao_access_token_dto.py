import time
from dataclasses import dataclass


@dataclass(frozen=True)
class KaKaoAccessTokenDto:
    access_token: str
    token_type: str
    refresh_token: str
    id_token: str
    expires_in: int
    scope: list[str]
    refresh_token_expires_in: int

    """ Example
    {
        "access_token": "J...w",
        "token_type": "bearer",
        "refresh_token": "...",
        "id_token": "ey...w",
        "expires_in": 21599,
        "scope": "age_range birthday account_email profile_image gender birthyear openid profile_nickname name phone_number",
        "refresh_token_expires_in": 5183999
    }
    """

    def expires_in_timestamp(self) -> int:
        return time.time() + self.expires_in
