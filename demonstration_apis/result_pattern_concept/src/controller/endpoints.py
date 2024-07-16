from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from src.contrib.response import AbstractExceptionResponse, ResultsResponse
from src.domain.service import ResourceService
from pydantic import BaseModel

result_pattern_concept_router = APIRouter(prefix="/api/v1/concept", tags=['RESULT_PATTERN'])


class Request(BaseModel):
    id: int
    content: str


@result_pattern_concept_router.post(
    path=''
)
def result_pattern_concept_api(
        request: Request,
        resource_service: ResourceService = Depends(ResourceService)
):
    result = resource_service.save(pk=request.id, content=request.content)
    if result.has_failure():
        return ResultsResponse(errors=result.failure)

    return JSONResponse(status_code=200, content={})
