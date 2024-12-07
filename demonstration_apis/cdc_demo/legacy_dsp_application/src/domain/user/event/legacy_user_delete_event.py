import datetime

from .legacy_user_event import LegacyUserEvent


class LegacyUserDeleteEvent(LegacyUserEvent):

    def occured_on(self) -> datetime.datetime:
        return self.user.deleted_at
