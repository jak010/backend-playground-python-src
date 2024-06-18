import uuid
from typing import Literal

from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse

from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.voguekorea.voguekorea_usecase import VogueKoreaUsecase

voguekorea_router = APIRouter(tags=["VogueKorea"], prefix="/api")


@voguekorea_router.get(path="/voguekorea")
def vogue_korea_contenst_list(
        sort_key: Literal["id", "reference_date"] = Query(default="id"),
        sort_type: Literal["DESC", "ASC"] = Query(default="DESC"),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10, ge=10, le=30),
        usecase: USECASE_TYPE = Depends(VogueKoreaUsecase),
):
    voguekorea_contents, voguekorea_contents_count = usecase.get_content_list(
        sort_key=sort_key,
        sort_type=sort_type,
        page=page,
        item_per_page=item_per_page
    )
    return JSONResponse(
        status_code=200,
        content={
            "sort_key": sort_key,
            "sort_type": sort_type,
            "page": page,
            "item_per_page": item_per_page,
            "total_count": voguekorea_contents_count,
            "items": [
                {
                    "id": voguekorea_content.id,
                    "trace_id": voguekorea_content.trace_id,
                    "reference_id": voguekorea_content.reference_id,
                    "reference_date": voguekorea_content.reference_date.isoformat(),
                    "reference_link": voguekorea_content.reference_link,
                    "thumbnail": voguekorea_content.thumbnail,
                    "is_convert": voguekorea_content.is_convert,
                    "title": voguekorea_content.title,
                }
                for voguekorea_content in voguekorea_contents
            ],
        },
    )


@voguekorea_router.get(path="/voguekorea/{trace_id:str}")
def vogue_korea_contenst_retreieve(
        trace_id: str = Path(), usecase: USECASE_TYPE = Depends(VogueKoreaUsecase)
):
    voguekorea_content = usecase.get_content(trace_id=trace_id)
    return JSONResponse(
        content={
            "trace_id": voguekorea_content.trace_id,
            "reference_id": voguekorea_content.reference_id,
            "reference_date": voguekorea_content.reference_date.isoformat(),
            "reference_link": voguekorea_content.reference_link,
            "thumbnail": voguekorea_content.thumbnail,
            "is_convert": voguekorea_content.is_convert,
            "title": voguekorea_content.title,
            "content": voguekorea_content.content,
        }
    )


@voguekorea_router.post(path="/voguekorea/{trace_id:str}/convert")
def vogue_korea_content_convert(
        trace_id: uuid.UUID = Path(), usecase: USECASE_TYPE = Depends(VogueKoreaUsecase)
):
    result = usecase.convert(trace_id=trace_id)
    if result is None:
        return JSONResponse(status_code=200, content={"msg": "alreday converted"})

    return JSONResponse(status_code=201, content=result)
