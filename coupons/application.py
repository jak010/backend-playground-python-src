from fastapi import FastAPI
from fastapi.responses import JSONResponse

from config import orm
from src.controller import root_router
from src.entity import CouponEntity, CouponIssueEntity


def bootstrapping():
    from sqlalchemy.orm import registry
    orm_mapping = registry()
    orm_mapping.map_imperatively(CouponEntity, orm.Coupon)
    orm_mapping.map_imperatively(CouponIssueEntity, orm.CouponIssue)
    return orm_mapping


def exception_handler(req, exc):
    print(req, exc)
    return JSONResponse(status_code=400, content={})


class CouponIssuranceApplication:
    app = FastAPI(
        title="쿠폰 발급 API"
    )

    @classmethod
    def exception_handler(cls):
        cls.app.add_exception_handler(Exception, exception_handler)

    @classmethod
    def run_servier(cls, *args, **kwargs):
        bootstrapping()

        cls.exception_handler()
        cls.app.include_router(root_router)

        return cls.app


coupon_issurance_application = CouponIssuranceApplication().run_servier()
