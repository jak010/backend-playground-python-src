from typing import Callable

from dependency_injector.wiring import Provide
from fastapi import Response, Request
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from libs.abstract.event_dispatcher import EventHandler
from settings.container.db_container import DataBaseContainer
from settings.container.event_container import EventContainer


class ExceptionHandlerRoute(APIRoute):
    session: Session = Provide[DataBaseContainer.session]
    event_handler: EventHandler = Provide[EventContainer.handler]

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:

            try:
                response: Response = await original_route_handler(request)
                if response.status_code == 200:

                    self.event_handler.emit()  # event dispatch
                    self.session.commit()
                else:
                    self.session.rollback()
                return response

            except Exception as e:
                self.session.rollback()
                raise e

        return custom_route_handler
