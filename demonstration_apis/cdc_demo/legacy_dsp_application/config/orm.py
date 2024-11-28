# coding: utf-8
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class LegacyUser(Base):
    __tablename__ = 'legacy_users'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
