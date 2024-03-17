# coding: utf-8
from sqlalchemy import CHAR, Column, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Member(Base):
    __tablename__ = 'member'

    pk = Column(INTEGER(1), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False)
    name = Column(String(32))
    age = Column(INTEGER(1))
    address1 = Column(String(1024))
    address2 = Column(String(1024))


class MemberProfile(Base):
    __tablename__ = 'member_profile'

    pk = Column(INTEGER(1), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    description = Column(String(32))


class PostComment(Base):
    __tablename__ = 'post_comments'

    pk = Column(INTEGER(10), primary_key=True)
    post_id = Column(INTEGER(1), nullable=False)
    created_at = Column(INTEGER(1), server_default=text("'0'"))


class Post(Base):
    __tablename__ = 'posts'

    pk = Column(INTEGER(10), primary_key=True)
    like = Column(INTEGER(10), server_default=text("'0'"))
    version = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    modified_at = Column(INTEGER(1), server_default=text("'0'"))
