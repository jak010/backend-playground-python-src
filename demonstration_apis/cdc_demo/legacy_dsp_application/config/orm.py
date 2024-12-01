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


class LegacyCampaign(Base):
    __tablename__ = 'legacy_campaigns'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    user_id = Column(INTEGER(11), nullable=False)
    budget = Column(INTEGER(11), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class LegacyAdgroup(Base):
    __tablename__ = 'legacy_adgroup'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    campaign_id = Column(INTEGER(11), nullable=False)
    user_id = Column(INTEGER(11), nullable=False)
    link_url = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
