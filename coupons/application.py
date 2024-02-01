from fastapi import FastAPI

from src.controller import root_router


class CouponIssuranceApplication:
    app = FastAPI(
        title="쿠폰 발급 API"
    )

    def __call__(self, *args, **kwargs):
        self.app.include_router(root_router)

        return self.app


coupon_issurance_application = CouponIssuranceApplication()
