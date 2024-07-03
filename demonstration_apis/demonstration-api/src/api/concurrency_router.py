import threading
import time

from fastapi import APIRouter
from fastapi.responses import JSONResponse

nonblock_router = APIRouter(tags=["NonBlock"], prefix="/api/v1/non-block")


class BackgroundThread(threading.Thread):
    """ Basic """
    daemon = True

    def __init__(self, xid):
        self.xid = xid
        super().__init__()

    def run(self) -> None:
        time.sleep(self.xid)
        print("Hello", self.xid)


@nonblock_router.get("/test")
def read_burgers():
    for x in range(100_000_000):
        pass

    ths = [BackgroundThread(1), BackgroundThread(2), BackgroundThread(3)]  # Case01, Thread를 실행시키고 Response를 반환한다.

    for th in ths:
        th.start()

    return JSONResponse(status_code=200, content={})
