from typing import Callable

from dependency_injector.wiring import Provide
from fastapi import Response, Request
from fastapi.routing import APIRoute

from src.config.container.database_container import DataBaseContainer


class TransactionRoute(APIRoute):
    session = Provide[DataBaseContainer.session]

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                response: Response = await original_route_handler(request)

                if response.status_code != 200:
                    self.session.rollback()
                    return response
                self.session.flush()
                self.session.commit()
                return response
            except Exception as e:
                self.session.rollback()
                raise e
            finally:
                self.session.close()

        return custom_route_handler
