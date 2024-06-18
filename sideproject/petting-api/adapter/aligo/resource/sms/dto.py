import dataclasses


@dataclasses.dataclass
class SMSSendResponseDto:
    result_code: int
    message: str
    msg_id: int
    success_cnt: int
    error_cnt: int
    msg_type: str
    """Response Data
    {
        'result_code': '1', 'message': 'success', 'msg_id': '771023557', 'success_cnt': 1, 'error_cnt': 0, 'msg_type': 'SMS'
    }
    """
