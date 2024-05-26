from library.http.error import NotFound


class MemberNotFound(NotFound):
    ERROR_CODE = 404_001
    MESSAGE = "Member NotFound"
