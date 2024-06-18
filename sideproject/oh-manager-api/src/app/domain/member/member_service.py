import re
import bcrypt


class MemberService:

    @staticmethod
    def encryption_password(password) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

    @staticmethod
    def check_password(password: str, hased_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hased_password.encode("utf-8"))

    @staticmethod
    def validate_email(member_email) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # 정규표현식 검증
        if re.match(pattern, member_email):
            return True
        else:
            return False
