from __future__ import annotations

import datetime

import nanoid as _nanoid

from libs.abstract.abstract_entity import AbstractEntity
from libs.utils import time_utils
from src.social.enums import SocialInviteRequestStatus


class SocialEntity(AbstractEntity):
    sender: str
    receiver: str
    status: str

    @classmethod
    def new(
            cls,
            sender: str,
            receiver: str,
            status: SocialInviteRequestStatus,
    ) -> SocialEntity:
        return cls(
            nanoid=_nanoid.generate(size=24),
            sender=sender,
            receiver=receiver,
            status=status,
            created_at=time_utils.now(),
            modified_at=time_utils.now()
        )

    def approval(self):
        self.status = SocialInviteRequestStatus.APPROVAL.value
        self.modified_at = datetime.datetime.now()

    def reject(self):
        self.status = SocialInviteRequestStatus.REJECT.value
        self.modified_at = datetime.datetime.now()
