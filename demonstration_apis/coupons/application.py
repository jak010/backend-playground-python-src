from fastapi import FastAPI
from fastapi.responses import JSONResponse

from config.settings import lifespan
from src.controller import root_router
import multiprocessing


def exception_handler(req, exc):
    return JSONResponse(status_code=400, content={})


class CouponIssuranceApplication:
    app = FastAPI(
        title="쿠폰 발급 API",
        lifespan=lifespan
    )

    @classmethod
    def exception_handler(cls):
        cls.app.add_exception_handler(Exception, exception_handler)

    def consumer(self):
        from src.consumer.coupon_issue_listener import CouponIssueListener
        from apscheduler.schedulers.background import BackgroundScheduler

        coupon_issue_lister = CouponIssueListener()

        sched = BackgroundScheduler(timezone='Asia/Seoul')
        sched.add_job(coupon_issue_lister.issue, 'interval', seconds=1, id='test')
        sched.start()

    def __call__(self, *args, **kwargs):
        self.exception_handler()
        self.app.include_router(root_router)

        self.consumer()
        return self.app


coupon_issurance_application = CouponIssuranceApplication()
