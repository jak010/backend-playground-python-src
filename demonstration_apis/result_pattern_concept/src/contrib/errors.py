class AbstractError(Exception):
    CODE = 0
    MESSAGE = ''

    def __init__(self, message=None):
        self.message = message
        super().__init__()


class NotExistError(AbstractError):
    CODE = 40001
    MESSAGE = 'Not Exist'


class DuplicatedError(AbstractError):
    CODE = 40002
    MESSAGE = 'Duplicated'
