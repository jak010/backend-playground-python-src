from typing import Literal

from fastapi import Form
from fastapi.responses import JSONResponse

from . import webhook_router


@webhook_router.post(
    path=""
)
def member_agreement_service_update(
        imp_uid: str = Form(),  # 결제번호
        merchant_uid: str = Form(),  # 주문번호
        status: Literal['paid', 'ready', 'failed', 'cancelled'] = Form(),  # 결제결과
):
    """
    https://developers.portone.io/docs/ko/result/webhook?v=v1
    https://admin.portone.io/integration-v2/manage/webhook
    """

    print(imp_uid)
    print(merchant_uid)
    print(status)
    return JSONResponse(status_code=200, content={})
