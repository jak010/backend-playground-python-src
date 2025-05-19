from sqlalchemy import CHAR, Column, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Member(Base):
    __tablename__ = 'member'

    pk = Column(INTEGER(10), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False)
    name = Column(String(32))
    age = Column(TINYINT(3))
    address1 = Column(String(1024))
    address2 = Column(String(1024))


class MemberProfile(Base):
    __tablename__ = 'member_profile'

    pk = Column(INTEGER(1), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    description = Column(String(32))