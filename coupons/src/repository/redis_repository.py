from __future__ import annotations
import dataclasses
import json

from config.settings import redis_client
from src.utils import CouponRedisUtils
from redis.commands.core import Script
from enum import Enum
from src.exceptions import CouponIssueException, ErroCode


@dataclasses.dataclass
class CouponIssueRequestDto:
    coupon_id: int
    user_id: int

    def to_dict(self):
        return dataclasses.asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())


class CouponIssueRequestCode(Enum):
    SUCCESS = 1
    DUPLICATE_COUPON_ISSUE = 2
    INVALIDE_COUPON_ISSUE_QUANTITY = 3

    @classmethod
    def find(cls, code):
        code_value = int(code)
        if code_value == 1:
            return cls.SUCCESS
        if code_value == 2:
            return cls.DUPLICATE_COUPON_ISSUE
        if code_value == 3:
            return cls.INVALIDE_COUPON_ISSUE_QUANTITY
        raise Exception("존재하지 않는코드이다.")

    @classmethod
    def check_request_reust(cls, code: CouponIssueRequestCode):
        if code == code.INVALIDE_COUPON_ISSUE_QUANTITY:
            raise CouponIssueException(ErroCode.INVALID_COUPON_ISSUE_QUANTITY, "발급 가능한 수량을 초과")
        if code == code.DUPLICATE_COUPON_ISSUE:
            raise CouponIssueException(ErroCode.DUPLICATE_COUPON_ISSUE, "이미 발급 요청된 쿠폰입니다.")


class RedisRepository:

    def __init__(self):
        self.client = redis_client()

    def zadd(self, key: str, value: dict) -> bool:
        return self.client.zadd(key, value, nx=True)  # NX: 데이터가 없는경우만 처리 , 있는경우 무시

    def sadd(self, key: str, value: str):
        return self.client.sadd(key, value)

    def scard(self, key: str):
        return self.client.scard(key)

    def sismember(self, key, value) -> bool:
        return self.client.sismember(key, value)

    # queue
    def rpush(self, key, value):
        return self.client.rpush(key, value)

    def lpop(self, key):
        return self.client.lpop(key)

    def clear(self, key):
        return self.client.delete(key)

    def lsize(self, key):
        return self.client.llen(name=key)

    def lindex(self, key, index):
        return self.client.lindex(name=key, index=index)

    # def lpop(self, key):
    #     return self.client.lock(name=key)

    def issu_request(self, coupon_id, user_id, total_issue_quantity):
        issue_request_key = CouponRedisUtils.get_issue_request_key(coupon_id)
        issue_request_queue_key = CouponRedisUtils.get_issue_request_queue_key()

        scripts = Script(script=self.issue_request_script(), registered_client=self.client)
        code = scripts(
            keys=[issue_request_key, issue_request_queue_key],
            args=[user_id, total_issue_quantity, CouponIssueRequestDto(coupon_id=coupon_id, user_id=user_id).to_json()],
        )

        CouponIssueRequestCode.check_request_reust(
            code=CouponIssueRequestCode.find(code=code)
        )

    def issue_request_script(self):
        scripts = """
            if redis.call('SISMEMBER', KEYS[1], ARGV[1]) == 1 then
                return '2'
            end
            
            if tonumber( ARGV[2] ) > redis.call('SCARD', KEYS[1]) then
                redis.call('SADD', KEYS[1], ARGV[1])
                redis.call('RPUSH', KEYS[2], ARGV[3])
                return '1'
            end            
            
            return '3'                        
        """
        return scripts
