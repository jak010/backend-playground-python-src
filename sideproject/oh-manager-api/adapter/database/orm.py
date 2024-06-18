# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Index, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Member(Base):
    __tablename__ = 'member'

    id = Column(INTEGER(1), primary_key=True)
    email = Column(String(64), nullable=False, unique=True)
    password = Column(CHAR(60), nullable=False)
    is_active = Column(TINYINT(1), comment='0:비활성화, 1:활성화')
    joined_at = Column(INTEGER(1), nullable=False)
    created_at = Column(INTEGER(1), nullable=False)
    modified_at = Column(INTEGER(1), nullable=False)


class Verification(Base):
    __tablename__ = 'verification'

    id = Column(INTEGER(1), primary_key=True)
    sender = Column(String(128), nullable=False)
    receiver = Column(String(128), nullable=False)
    code = Column(CHAR(6), nullable=False)
    type = Column(String(10), nullable=False)
    status = Column(String(10), nullable=False, comment='0:전송, 1:인증완료, 2:인증파기')
    expired_at = Column(INTEGER(1), nullable=False)
    created_at = Column(INTEGER(1), nullable=False)
    modified_at = Column(INTEGER(1), nullable=False)


class Session(Base):
    __tablename__ = 'session'

    id = Column(INTEGER(1), primary_key=True)
    session_id = Column(CHAR(36), nullable=False)
    member_id = Column(CHAR(36), nullable=False)
    iat = Column(INTEGER(1), nullable=False)
    exp = Column(INTEGER(1), nullable=False)
    created_at = Column(INTEGER(1), nullable=False)


class Profile(Base):
    __tablename__ = 'profile'
    __table_args__ = (
        Index('profile_index', 'member_id', 'name', unique=True),
    )

    id = Column(INTEGER(1), primary_key=True)
    member_id = Column(CHAR(36), nullable=False, comment='ref, member.id')
    name = Column(String(64), nullable=False)
    description = Column(Text)
    profile_url = Column(String(255))
    age = Column(DateTime)
    gender = Column(String(36))
    body_weight = Column(INTEGER(1))
    body_height = Column(INTEGER(1))
    country = Column(String(36))
    address = Column(String(128))
    instargram_url = Column(String(255))
    facebook_url = Column(String(255))
    twitter_url = Column(String(255))
    profile_image = Column(String(255))
    created_at = Column(INTEGER(1), nullable=False)
    modified_at = Column(INTEGER(1), nullable=False)


class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(BIGINT(1), primary_key=True)
    uid = Column(String(32), nullable=False, comment='플랫폼에서 구분되는 게시번호')
    platform = Column(String(32), nullable=False, comment='수집 플랫폼')
    is_remake = Column(TINYINT(1), server_default=text("'0'"))
    title = Column(String(255))
    content = Column(Text)
    category = Column(String(255))
    author = Column(String(255))
    reward = Column(String(255))
    link = Column(String(1028))
    end_date = Column(DateTime)
    created_at = Column(INTEGER(1), nullable=False)
    modified_at = Column(INTEGER(1), nullable=False)


class Submission(Base):
    __tablename__ = 'submissions'
    __table_args__ = (
        Index('submission_index', 'audition_id', 'member_id', unique=True),
    )

    id = Column(INTEGER(1), primary_key=True)
    audition_id = Column(INTEGER(1), nullable=False, comment='auditions .auditions_id')
    member_id = Column(CHAR(36), nullable=False, comment='`member`.member_id')
    status = Column(String(32))
    created_at = Column(INTEGER(1), nullable=False)
    modified_at = Column(INTEGER(1), nullable=False)
