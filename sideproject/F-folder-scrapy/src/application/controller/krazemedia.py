from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import JSONResponse

from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.krazemedia.krazemedia_usecase import KrazeMediaUsecase

krazemedia_rotuer = APIRouter(tags=['KrazeMedia'], prefix="/api")


@krazemedia_rotuer.get(path="/krazemedia")
def krazemedia_list(
        sort_key: Literal['id', 'reference_date'] = Query(default='id'),
        sort_type: Literal['DESC', 'ASC'] = Query(default='DESC'),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10),

        usecase: USECASE_TYPE = Depends(KrazeMediaUsecase)
):
    krazemedia_contents_list, krazemedia_contents_count = usecase.get_content_list(
        page=page,
        item_per_page=item_per_page,
        sort_key=sort_key,
        sort_type=sort_type
    )

    return JSONResponse(status_code=200, content={
        "page": page,
        "item_per_page": item_per_page,
        "total_count": krazemedia_contents_count,
        "items": [{
            "trace_id": krazemedia.trace_id,
            "reference_id": krazemedia.reference_id,
            "reference_date": krazemedia.reference_date.isoformat(),
            "reference_link": krazemedia.reference_link,
            "thumbnail": krazemedia.thumbnail,
            "is_convert": krazemedia.is_convert,
            "title": str(krazemedia.title)
        } for krazemedia in krazemedia_contents_list]})


@krazemedia_rotuer.get(path="/krazemedia/{trace_id:str}")
def krazemedia_retreieve(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(KrazeMediaUsecase)
):
    krazemedia = usecase.get_content(trace_id=trace_id)
    if krazemedia is None:
        return JSONResponse(status_code=404, content={})

    return JSONResponse(status_code=200, content={
        "trace_id": krazemedia.trace_id,
        "reference_id": krazemedia.reference_id,
        "reference_date": krazemedia.reference_date.isoformat(),
        "reference_link": krazemedia.reference_link,
        "thumbnail": krazemedia.thumbnail,
        "is_convert": krazemedia.is_convert,
        "title": krazemedia.title,
        "content": krazemedia.content
    })


@krazemedia_rotuer.post(path="/krazemedia/{trace_id:str}/convert")
def krazemedia_convert(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(KrazeMediaUsecase)
):
    return JSONResponse(status_code=200, content=usecase.convert(trace_id=trace_id))
