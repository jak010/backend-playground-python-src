from fastapi import FastAPI
from fastapi.responses import JSONResponse

from config.settings import lifespan
from src.controller import root_router


def exception_handler(req, exc):
    print(req, exc)
    return JSONResponse(status_code=400, content={})


class CouponIssuranceApplication:
    app = FastAPI(
        title="쿠폰 발급 API",
        lifespan=lifespan
    )

    @classmethod
    def exception_handler(cls):
        cls.app.add_exception_handler(Exception, exception_handler)

    @classmethod
    def run_servier(cls, *args, **kwargs):
        cls.exception_handler()
        cls.app.include_router(root_router)

        return cls.app


coupon_issurance_application = CouponIssuranceApplication().run_servier()
