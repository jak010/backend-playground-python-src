# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CouponIssue(Base):
    __tablename__ = 'coupon_issues'
    __table_args__ = (
        Index('coupon_issue_index', 'coupon_id', 'user_id', unique=True),
        {'comment': '쿠폰 발급 내역'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='ID')
    coupon_id = Column(BIGINT(20), nullable=False, comment='쿠폰 ID')
    user_id = Column(BIGINT(20), nullable=False, comment='사용자 ID')
    date_issued = Column(DATETIME(fsp=6), nullable=False, comment='발급 일자')
    date_used = Column(DATETIME(fsp=6), comment='사용 일자')
    date_created = Column(DATETIME(fsp=6), nullable=False)
    date_updated = Column(DATETIME(fsp=6), nullable=False, comment='업데이트 일자')


class Coupon(Base):
    __tablename__ = 'coupons'
    __table_args__ = {'comment': 'ì¿\xa0í\x8f° ì\xa0•ì±…'}

    id = Column(BIGINT(20), primary_key=True)
    title = Column(String(255), nullable=False, comment='ì¿\xa0í\x8f° ì\xa0œëª©')
    coupon_type = Column(String(255), nullable=False, comment='ì¿\xa0í\x8f° ì¢…ë¥˜')
    total_quantity = Column(INTEGER(11), nullable=False, comment='ë°œê¸‰ ì´\x9d ìˆ˜ëŸ‰')
    issued_quantity = Column(INTEGER(11), comment='ì¿\xa0í\x8f° ë°œê¸‰ ìµœëŒ€ ìˆ˜ëŸ‰')
    discount_amount = Column(INTEGER(11), nullable=False, comment='í•\xa0ì\x9d¸ ê¸ˆì•¡')
    min_available_amount = Column(INTEGER(11), nullable=False, comment='ìµœì†Œ ì‚¬ìš© ê¸ˆì•¡')
    date_issue_start = Column(DATETIME(fsp=6), nullable=False, comment='ì¿\xa0í\x8f° ë°œê¸‰ ì‹œìž‘ì\x9d¼')
    date_issue_end = Column(DATETIME(fsp=6), nullable=False, comment='ì¿\xa0í\x8f° ë°œê¸‰ ì¢…ë£Œì\x9d¼')
    date_created = Column(DATETIME(fsp=6), nullable=False)
    date_updated = Column(DATETIME(fsp=6), nullable=False)
