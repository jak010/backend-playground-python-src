from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse

from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.eyesmag.eyesmag_usecase import EyesMagUsecase

eyesmag_rotuer = APIRouter(tags=['EyesMag'], prefix="/api")


@eyesmag_rotuer.get(path="/eyesmag")
def eyesmag_list(
        sort_key: Literal['id', 'reference_date'] = Query(default='id'),
        sort_type: Literal['DESC', 'ASC'] = Query(default='DESC'),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10, ge=10, le=30),

        usecase: USECASE_TYPE = Depends(EyesMagUsecase)
):
    eyesmags_contents, eyesmags_contents_count = usecase.get_content_list(
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
            "total_count": eyesmags_contents_count,
            "items": [{
                "id": eyesmags.id,
                "trace_id": eyesmags.trace_id,
                "reference_id": eyesmags.reference_id,
                "reference_date": eyesmags.reference_date.isoformat(),
                "reference_link": eyesmags.reference_link,
                "thumbnail": eyesmags.thumbnail,
                "is_convert": eyesmags.is_convert,
                "title": eyesmags.title
            } for eyesmags in eyesmags_contents]})


@eyesmag_rotuer.get(path="/eyesmag/{trace_id:str}")
def eyesmag_retreieve(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(EyesMagUsecase)
):
    eyesmag = usecase.get_content(trace_id=trace_id)
    if eyesmag is None:
        return JSONResponse(status_code=404, content={})

    return JSONResponse(status_code=200, content={
        "id": eyesmag.id,
        "trace_id": eyesmag.trace_id,
        "reference_id": eyesmag.reference_id,
        "reference_date": str(eyesmag.reference_date),
        "reference_link": eyesmag.reference_link,
        "thumbnail": eyesmag.thumbnail,
        "is_convert": eyesmag.is_convert,
        "title": eyesmag.title,
        "content": eyesmag.content
    })


@eyesmag_rotuer.post(path="/eyesmag/{trace_id:str}/convert")
def eyesmag_content_convert(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(EyesMagUsecase)
):
    return JSONResponse(status_code=200, content=usecase.convert(trace_id=trace_id))
