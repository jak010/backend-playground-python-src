# coding: utf-8
from sqlalchemy import CHAR, Column, Date, DateTime, Integer, String, Text, text, SMALLINT
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, MEDIUMTEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Eyesmag(Base):
    __tablename__ = 'eyesmag'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(String(36))
    reference_date = Column(DateTime, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    thumbnail = Column(String(256), nullable=False)


class Fashionchingu(Base):
    __tablename__ = 'fashionchingu'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(INTEGER, unique=True)
    reference_date = Column(DateTime, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    thumbnail = Column(String(256), nullable=False)


class Fashioninsight(Base):
    __tablename__ = 'fashioninsight'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(INTEGER, nullable=False, unique=True)
    reference_date = Column(DateTime, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    thumbnail = Column(String(256), nullable=False)


class Harpersbazaar(Base):
    __tablename__ = 'harpersbazaar'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(INTEGER, unique=True)
    reference_date = Column(Date, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(MEDIUMTEXT, nullable=False)
    thumbnail = Column(String(256), nullable=False)


class Kmode(Base):
    __tablename__ = 'kmodes'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(BIGINT(unsigned=True), unique=True)
    reference_date = Column(DateTime, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    thumbnail = Column(Text, nullable=False)


class Krazefashion(Base):
    __tablename__ = 'krazefashion'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(BIGINT)
    reference_date = Column(DateTime, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), unique=True)
    content = Column(Text, nullable=False)
    thumbnail = Column(Text, nullable=False)


class Krazemedia(Base):
    __tablename__ = 'krazemedia'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(BIGINT)
    reference_date = Column(DateTime, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), unique=True)
    content = Column(Text, nullable=False)
    thumbnail = Column(Text, nullable=False)


class Post(Base):
    __tablename__ = 'post'

    post_id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    views = Column(INTEGER, nullable=False, server_default=text("'0'"))
    is_deleted = Column(TINYINT(1), server_default=text("'0'"), comment='0:미삭제, 1:삭제')
    is_temporary = Column(TINYINT(1), server_default=text("'0'"))
    title = Column(String(5012), nullable=False)
    content = Column(Text, comment='llm으로 변환된 콘텐츠')
    keyword = Column(Text, comment='llm으로 변환된 키워드')
    platform = Column(String(36), nullable=False)
    reference_link = Column(String(5012), nullable=False)
    thumbnail = Column(String(1024), nullable=False)
    created_at = Column(INTEGER, nullable=False)
    modified_at = Column(INTEGER, nullable=False)


class Seoulinspired(Base):
    __tablename__ = 'seoulinspired'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(INTEGER, unique=True)
    reference_date = Column(Date, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(MEDIUMTEXT, nullable=False)
    thumbnail = Column(String(256), nullable=False)


class Unnielook(Base):
    __tablename__ = 'unnielooks'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(INTEGER, unique=True)
    reference_date = Column(Date, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(MEDIUMTEXT, nullable=False)
    thumbnail = Column(String(256), nullable=False)


class Voguekorea(Base):
    __tablename__ = 'voguekorea'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(INTEGER, nullable=False, unique=True)
    reference_date = Column(DateTime, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(MEDIUMTEXT, nullable=False)
    thumbnail = Column(String(256), nullable=False)


class Yesstyle(Base):
    __tablename__ = 'yesstyle'

    id = Column(INTEGER, primary_key=True)
    trace_id = Column(CHAR(36), nullable=False)
    is_convert = Column(TINYINT, server_default=text("'0'"))
    reference_id = Column(Integer, unique=True)
    reference_date = Column(DateTime, nullable=False)
    reference_link = Column(String(5012), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    thumbnail = Column(String(256), nullable=False)


class PostHistory(Base):
    __tablename__ = 'post_history'

    id = Column(INTEGER(1), primary_key=True)
    post_id = Column(INTEGER(1), comment='ref, post.post_id')
    ip = Column(INTEGER(1), nullable=False)
    port = Column(SMALLINT(), nullable=False)
    referrer = Column(String(2048), nullable=False)
    useragent = Column(String(2048), nullable=False)
    created_at = Column(INTEGER(1), nullable=False)
