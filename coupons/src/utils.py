class CoutponRedisUtils:

    @staticmethod
    def get_issue_request_key(coupon_id: str):
        return f'issue.request.coupon_id={coupon_id}'

    @staticmethod
    def get_issue_request_queue_key():
        return f"issue.request"
