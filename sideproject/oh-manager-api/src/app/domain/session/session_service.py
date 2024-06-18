import time
import uuid

from src.app.domain.session.session_entity import SessionEntity
from src.libs import time_util


class SessionService:

    @staticmethod
    def create_session_for_one_hour(member_id) -> SessionEntity:
        _current_time = int(time.time())

        return SessionEntity.new(
            session_id=str(uuid.uuid4()),
            member_id=member_id,
            iat=_current_time,
            exp=_current_time + time_util.SECONDS_IN_ONE_HOUR
        )
