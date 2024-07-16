class Result:

    def __init__(self, success=None, data=None):
        self.success = success
        self.failure = []
        self.data = data

    def add_error(self, error):
        self.failure.append(error)
        return self

    def has_failure(self) -> bool:
        if self.failure:
            return True
        return False
