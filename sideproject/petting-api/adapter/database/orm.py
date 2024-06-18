# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Float, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Assessment(Base):
    __tablename__ = 'assessment'

    pk = Column(INTEGER(10), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False)
    member_id = Column(CHAR(24), nullable=False, unique=True, comment='ref, member.nanoid')
    status = Column(String(32), nullable=False, comment='WAIT, REJECT, APPROVE')
    reason = Column(String(1024))
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class Certification(Base):
    __tablename__ = 'certification'

    pk = Column(INTEGER(1), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False)
    member_id = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    phone = Column(String(20))
    type = Column(String(12), nullable=False, comment='ì\x9d¸ì¦\x9d íƒ€ìž…')
    code = Column(String(12), nullable=False, comment='ì\x9d¸ì¦\x9d ì½”ë“œ')
    status = Column(String(12), nullable=False, comment='ì§„í–‰ ìƒ\x81íƒœ')
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class ChatRoom(Base):
    __tablename__ = 'chat_room'

    pk = Column(INTEGER(10), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class ChatRoomMember(Base):
    __tablename__ = 'chat_room_member'

    pk = Column(INTEGER(10), primary_key=True)
    member_id = Column(CHAR(24), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class Member(Base):
    __tablename__ = 'member'

    pk = Column(INTEGER(1), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False)
    name = Column(String(32), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    channel = Column(String(128), nullable=False)
    referral_code = Column(CHAR(12))
    is_onboard = Column(TINYINT(1), server_default=text("'0'"))
    phone = Column(String(20), nullable=False)
    coin = Column(INTEGER(1), server_default=text("'0'"))
    certificate_of_phone = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    certificate_of_phone_registered_at = Column(DateTime)
    terms_of_age = Column(TINYINT(1), nullable=False)
    terms_of_agreement = Column(TINYINT(1), nullable=False)
    terms_of_privacy = Column(TINYINT(1), nullable=False)
    terms_of_geolocation = Column(TINYINT(1), nullable=False)
    terms_of_marketing = Column(TINYINT(1))
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class MemberAsset(Base):
    __tablename__ = 'member_asset'

    pk = Column(INTEGER(1), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    type = Column(String(12), nullable=False)
    issued_quantity = Column(INTEGER(1), server_default=text("'0'"))
    reason = Column(String(1024))
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class MemberProfile(Base):
    __tablename__ = 'member_profile'

    pk = Column(INTEGER(1), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    nickname = Column(String(64), nullable=False, unique=True)
    description = Column(String(300))
    address = Column(String(1024))
    region1 = Column(String(128))
    region2 = Column(String(128))
    region3 = Column(String(128))
    road_name = Column(String(128))
    latitude = Column(Float(10, True), comment='Ã¬Å“â€žÃ«Â\x8fâ€ž')
    longitude = Column(Float(10, True), comment='ÃªÂ²Â½Ã«Â\x8fâ€ž')
    job = Column(String(24))
    birthday = Column(DateTime, nullable=False)
    gender = Column(String(16), nullable=False)
    mbti = Column(CHAR(4))
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class Pet(Base):
    __tablename__ = 'pet'
    __table_args__ = (
        Index('pet_indexer_1', 'owner', 'name', unique=True),
    )

    pk = Column(INTEGER(10), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False)
    owner = Column(CHAR(24), nullable=False)
    name = Column(String(32), nullable=False)
    gender = Column(String(12), nullable=False)
    pdti = Column(String(32))
    pdti_type = Column(String(4))
    neutered_status = Column(String(4))
    breed = Column(String(128))
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class PetAttachment(Base):
    __tablename__ = 'pet_attachment'
    __table_args__ = (
        Index('pet_attachment_indexer_1', 'member_id', 'file_name', unique=True),
    )

    pk = Column(INTEGER(10), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False, comment='ref, pet.nanoid')
    member_id = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    attachment_type = Column(String(12), nullable=False)
    attachment_label = Column(String(12), nullable=False)
    s3_key = Column(String(512), comment='s3, saved key')
    file_name = Column(String(64), nullable=False, comment='s3, file_name')
    file_size = Column(INTEGER(1), nullable=False)
    content_type = Column(String(64), nullable=False, comment='content_type')
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class Session(Base):
    __tablename__ = 'session'

    pk = Column(INTEGER(10), primary_key=True)
    nanoid = Column(CHAR(24), nullable=False)
    member_id = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    channel = Column(String(24))
    channel_code = Column(String(1024))
    issued_time = Column(INTEGER(10), nullable=False)
    expire_time = Column(INTEGER(10), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)


class Social(Base):
    __tablename__ = 'social'

    pk = Column(INTEGER(10), primary_key=True)
    sender = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    receiver = Column(CHAR(24), nullable=False, comment='ref, member.nanoid')
    status = Column(String(12), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
