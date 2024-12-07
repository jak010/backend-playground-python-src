import datetime

from .legacy_user_event import LegacyUserEvent


class LegacyUserCreateEvent(LegacyUserEvent):

    def occured_on(self) -> datetime.datetime:
        return self.user.created_at
