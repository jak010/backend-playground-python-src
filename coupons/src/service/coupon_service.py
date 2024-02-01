from src.entity.coupon_entity import CouponIssueException, ErroCode, CouponEntity
from src.entity.coupon_issue_entity import CouponIssueEntity
from src.repository import CouponRepository, CouponIssueRepository


class CouPonIssueService:
    coupon_repository = CouponRepository()
    coupon_issue_repository = CouponIssueRepository()

    def issue_save(self):
        coupon_issue = CouponIssueEntity(coupon_id=1, user_id=2)
        self.coupon_issue_repository.save(coupon_issue)

    def issue(self, coupon_id: int, user_id: int):
        coupon = self.find_coupon(coupon_id=coupon_id)
        coupon.issue()
        self.save_coupon_issue(coupon_id=coupon_id, user_id=user_id)
        return coupon

    def find_coupon(self, coupon_id: int) -> CouponEntity:
        try:
            coupon = self.coupon_repository.find_by_id(coupon_id=coupon_id)
        except Exception as e:
            raise CouponIssueException(error_code=ErroCode.COUPON_NOT_EXIST.value, message="쿠폰이 존재하지 않습니다.")
        return coupon

    def save_coupon_issue(self, coupon_id: int, user_id: id):
        self._check_already_issuance(coupon_id=coupon_id, user_id=user_id)
        coupon_issue = CouponIssueEntity(coupon_id=coupon_id, user_id=user_id)
        return self.coupon_issue_repository.save(coupon_issue)

    def _check_already_issuance(self, coupon_id: int, user_id: int):
        issue = self.coupon_issue_repository.find_first_coupon_issue(coupon_id=coupon_id, user_id=user_id)
        if issue is not None:
            raise CouponIssueException(error_code=ErroCode.DUPLICATE_COUPON_ISSUE.value, message=f"이미 발급된 쿠폰입니다.{coupon_id, user_id}")
