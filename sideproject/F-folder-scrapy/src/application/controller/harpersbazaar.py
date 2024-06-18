from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse

from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.harpersbazaar.harpersbazaar_usecase import HarpersBazaarUsecase

harpersbazaar_rotuer = APIRouter(tags=['HarpersBazaar'], prefix="/api")


@harpersbazaar_rotuer.get(path="/harpersbazaar")
def harpersbazaar_list(
        sort_key: Literal['id', 'reference_date'] = Query(default='id'),
        sort_type: Literal['DESC', 'ASC'] = Query(default='DESC'),
        page: int = Query(default=1, ge=1),
        item_per_page: int = Query(default=10, ge=10, le=20),

        usecase: USECASE_TYPE = Depends(HarpersBazaarUsecase)
):
    harpersbazaars, harpersbazaar_content_count = usecase.get_content_list(
        sort_key=sort_key,
        sort_type=sort_type,
        page=page,
        item_per_page=item_per_page,
    )

    return JSONResponse(status_code=200, content={
        "page": page,
        "item_per_page": item_per_page,
        "sort_key": sort_key,
        "total_count": harpersbazaar_content_count,
        "items": [{
            "id": harpersbazaar.id,
            "trace_id": harpersbazaar.trace_id,
            "reference_id": harpersbazaar.reference_id,
            "reference_date": harpersbazaar.reference_date.isoformat(),
            "reference_link": harpersbazaar.reference_link,
            "thumbnail": harpersbazaar.thumbnail,
            "is_convert": harpersbazaar.is_convert,
            "title": harpersbazaar.title
        } for harpersbazaar in harpersbazaars]})


@harpersbazaar_rotuer.get(path="/harpersbazaar/{trace_id:str}")
def harpersbazaar_list(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(HarpersBazaarUsecase)
):
    harpersbazaar_content = usecase.get_content(trace_id=trace_id)
    if harpersbazaar_content is None:
        return JSONResponse(status_code=404, content={})

    return JSONResponse(status_code=200, content={
        "id": harpersbazaar_content.id,
        "trace_id": harpersbazaar_content.trace_id,
        "reference_id": harpersbazaar_content.reference_id,
        "reference_date": str(harpersbazaar_content.reference_date),
        "reference_link": harpersbazaar_content.reference_link,
        "thumbnail": harpersbazaar_content.thumbnail,
        "is_convert": harpersbazaar_content.is_convert,
        "title": harpersbazaar_content.title,
        "content": harpersbazaar_content.content
    })


@harpersbazaar_rotuer.post(path="/harpersbazaar/{trace_id:str}/convert")
def harpersbazaar_convert(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(HarpersBazaarUsecase)
):
    harpersbazaar_content = usecase.convert(trace_id=trace_id)

    return JSONResponse(status_code=200, content=harpersbazaar_content)
