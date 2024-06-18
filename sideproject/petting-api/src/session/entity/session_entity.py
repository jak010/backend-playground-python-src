from __future__ import annotations

import datetime
import json
import time
from typing import Optional

from libs.abstract.abstract_entity import AbstractEntity
from src.member.entity import MemberEntity
from src.session.value_object import SessionChannel, ChannelCode


class SessionEntity(AbstractEntity):
    member_id: str

    channel: str
    channel_code: str

    issued_time: int
    expire_time: int

    member: Optional[MemberEntity]

    @classmethod
    def new(
            cls,
            *,
            member_id: str,
            channel: SessionChannel,
            channel_code: str,
            expire_time: int
    ) -> SessionEntity:
        return cls(
            nanoid=cls.generate_nano_id(),
            member_id=member_id,
            channel=channel,
            channel_code=channel_code if channel_code is not None else None,
            issued_time=time.time(),
            expire_time=expire_time,
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now(),
        )

    @property
    def channel_code_to_json(self) -> ChannelCode:
        return json.loads(self.channel_code)
