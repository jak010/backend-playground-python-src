from src.infrastructure.inmemory_repository import InMemoryRepository
from src.contrib import result
from src.contrib import errors
from src.contrib.result import Result

from fastapi.exceptions import HTTPException


class ResourceService:
    repository = InMemoryRepository()

    def save(self, pk: int, content: str):
        _result = Result()

        resource = self.repository.find_by_id(id=pk)
        if not resource:
            _result.add_error(errors.NotExistError)

        item = self.repository.add(id=pk, content=content)
        if not item:
            _result.add_error(errors.DuplicatedError)

        return _result
