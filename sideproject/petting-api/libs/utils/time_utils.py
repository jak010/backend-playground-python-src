from datetime import datetime


def parse_birthday(birthyear: str, birthday: str) -> datetime:
    birth_string = f"{birthyear}-{birthday}"
    try:
        return datetime.strptime(birth_string, "%Y-%m%d")
    except ValueError:
        raise RuntimeError("잘못된 형식의 날짜입니다. 올바른 형식은 'YYYY-MMDD'입니다.")


def now() -> datetime:
    return datetime.now()
