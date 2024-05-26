# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Member(Base):
    __tablename__ = 'member'

    pk = Column(INTEGER(1), primary_key=True)
    name = Column(String(32))
    age = Column(INTEGER(1))
