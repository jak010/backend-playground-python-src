import datetime

import pytz

KST = datetime.timezone(datetime.timedelta(hours=9))

SECONDS_IN_ONE_HOUR = 3600


def midnight(date_time: datetime):
    """ 자정시간 구하기 """
    now = date_time.now()
    return datetime.datetime(now.year, now.month, now.day)


def epochtime_to_datetime(epoch_time: int):
    """ unix_time을 datetime으로 변경하기 """
    return datetime.datetime.utcfromtimestamp(int(epoch_time))


def midnight_kst() -> int:
    timezone = pytz.timezone("Asia/Seoul")

    current_date = datetime.datetime.now(timezone)

    today_midnight = datetime.datetime.combine(current_date, datetime.time.min)

    return int(today_midnight.timestamp())
