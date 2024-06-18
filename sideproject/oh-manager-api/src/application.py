from fastapi import FastAPI
from src.config.settings.base import patch_ioc, patch_controller, patch_orm


class Application:
    app = FastAPI(
        title="Oh Manager API",
        description="Oh Manager API Document"
    )

    def __call__(self, *args, **kwargs):
        patch_ioc()
        patch_controller(self.app)
        patch_orm()

        return self.app


Application = Application()
