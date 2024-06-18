from typing import Optional

from fastapi import HTTPException, status, Request
from fastapi.security import APIKeyHeader


class ApiKeyHeaderMiddleware(APIKeyHeader):

    def __init__(self):

        self.api_header_key = "access-token"

        super(ApiKeyHeaderMiddleware, self).__init__(
            name=self.api_header_key,
            scheme_name="AccessToken"
        )

    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)
        if not api_key:
            if self.auto_error:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized")
            else:
                return None
        return api_key
