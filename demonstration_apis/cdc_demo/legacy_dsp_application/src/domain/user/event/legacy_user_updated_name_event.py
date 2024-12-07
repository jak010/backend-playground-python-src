import datetime

from .legacy_user_event import LegacyUserEvent


class LegacyUserUpdatedNamedEvent(LegacyUserEvent):

    def occured_on(self) -> datetime.datetime:
        return self.user.updated_at
