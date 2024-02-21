from fastapi import FastAPI, Request, HTTPException
import asyncio
from src.controller import controller_router, websocket_router


def exception_handler(request: Request, exc: HTTPException):
    import sys
    sys.exit()


async def my_lifespan(app):
    print(f'startup lifespan')
    yield
    print('shutdown lifespan')


class PubSubApplication:
    app = FastAPI(lifespan=my_lifespan)

    def __call__(self, *args, **kwargs):
        # self.app.add_exception_handler(asyncio.exceptions.CancelledError, exception_handler)

        from fastapi.middleware.cors import CORSMiddleware

        origins = ["*"]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.app.include_router(controller_router)
        self.app.include_router(websocket_router)
        return self.app


pubsub_application = PubSubApplication()
