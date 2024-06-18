from __future__ import annotations

from io import current_task
from typing import TYPE_CHECKING

from sqlalchemy import pool
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.io import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker
)

if TYPE_CHECKING:
    pass

import logging

logger = logging.getLogger(__name__)


def context(drivername: str, username: str, password: str, database: str, host: str, port: int):
    url = URL.create(drivername=drivername,
                     username=username,
                     password=password,
                     database=database,
                     host=host,
                     port=port)
    async_engine = create_async_engine(url,
                                       echo=True,
                                       pool_recycle=3600,
                                       pool_size=4,
                                       pool_pre_ping=True,
                                       )

    async_session = async_scoped_session(async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=True,
        autocommit=False,
        autoflush=False
    ),
        scopefunc=current_task
    )

    return async_session

# class Database:
#
#     @classmethod
#     def context(cls,
#                 drivername: str,
#                 username: str,
#                 password: str,
#                 database: str,
#                 host: str,
#                 port: int,
#                 ):
#         url = URL.create(
#             drivername=drivername,
#             username=username,
#             password=password,
#             database=database,
#             host=host,
#             port=port
#         )
#
#         async_engine = create_async_engine(
#             url,
#             echo=True,
#             pool_recycle=3600,
#             pool_size=4,
#             pool_pre_ping=True,
#         )
#         async_session_local = async_sessionmaker(
#             bind=async_engine,
#             class_=AsyncSession,
#             expire_on_commit=True,
#         )
#         async_session = async_scoped_session(
#             async_session_local,
#             scopefunc=current_task
#         )
#
#         print(async_engine.pool.status())
#
#         yield async_session
#
#
