from typing import List, Dict

from fastapi.responses import JSONResponse


class BaseSuccessResponse(JSONResponse):
    STATUS_CODE: int = 200
    DATA = {}

    def __init__(self, data=None, *args, **kwargs):
        self.DATA = data
        super().__init__(
            status_code=self.STATUS_CODE,
            content=self.body()
        )

    @classmethod
    def body(cls):
        return {
            "status_code": cls.STATUS_CODE,
            "data": cls.DATA
        }


class PaginateReponse(BaseSuccessResponse):

    def __init__(self, page: int, per_page: int, total_count: int, data: List[Dict] = None):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.datas = [item for item in data]
        super().__init__(data)

    def body(self):
        return {
            "status_code": self.STATUS_CODE,
            "data": {
                "page": self.page,
                "per_page": self.per_page,
                "total_count": self.total_count,
                "items": self.datas
            }
        }
