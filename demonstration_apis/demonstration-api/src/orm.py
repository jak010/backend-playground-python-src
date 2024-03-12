# coding: utf-8
from sqlalchemy import CHAR, Column, MetaData, String, Table
from sqlalchemy.dialects.mysql import INTEGER

metadata = MetaData()


t_member = Table(
    'member', metadata,
    Column('pk', INTEGER(1), primary_key=True),
    Column('nanoid', CHAR(24), nullable=False),
    Column('name', String(32)),
    Column('age', INTEGER(1)),
    Column('address1', String(1024)),
    Column('address2', String(1024))
)


t_member_profile = Table(
    'member_profile', metadata,
    Column('pk', INTEGER(1), primary_key=True),
    Column('nanoid', CHAR(24), nullable=False, comment='ref, member.nanoid'),
    Column('description', String(32))
)
