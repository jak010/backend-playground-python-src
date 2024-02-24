# coding: utf-8
from sqlalchemy import CHAR, Column, String
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


class MemberProfile(Base):
    __tablename__ = 'member_profile'

    pk = Column(INTEGER(1), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    description = Column(String(32))
