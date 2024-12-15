from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

# from dependency_injector.wiring import Provide
#
# from .container import EventContainer

from src.application.events.handler import LegacyDomainEventListener


class ApplicationEventMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        print("Event Middleware Called Started")
        response: Response = await call_next(request)
        if response.status_code != 200:
            return response

        print("Event Middleware Invoke Stored Events")

        event_listener = LegacyDomainEventListener()
        event_listener.handle_event()

        return response
