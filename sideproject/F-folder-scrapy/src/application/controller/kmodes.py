from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import JSONResponse

from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.kmodes.kmodes_usecase import KmodesUsecase

kmodes_rotuer = APIRouter(tags=['Kmodes'], prefix="/api")


@kmodes_rotuer.get(path="/kmodes")
def kmodes_list(
        sort_key: Literal['id', 'reference_date'] = Query(default='id'),
        sort_type: Literal['DESC', 'ASC'] = Query(default='DESC'),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10),

        usecase: USECASE_TYPE = Depends(KmodesUsecase)
):
    kmodes_contents_list, kmodes_contents_count = usecase.get_content_list(
        page=page,
        item_per_page=item_per_page,
        sort_key=sort_key,
        sort_type=sort_type
    )

    return JSONResponse(status_code=200, content={
        "page": page,
        "item_per_page": item_per_page,
        "total_count": kmodes_contents_count,
        "items": [{
            "trace_id": kmodes.trace_id,
            "reference_id": kmodes.reference_id,
            "reference_date": str(kmodes.reference_date),
            "reference_link": kmodes.reference_link,
            "thumbnail": kmodes.thumbnail,
            "is_convert": kmodes.is_convert,
            "title": str(kmodes.title)
        } for kmodes in kmodes_contents_list]})


@kmodes_rotuer.get(path="/kmodes/{trace_id:str}")
def kmodes_retreieve(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(KmodesUsecase)
):
    kmodes = usecase.get_content(trace_id=trace_id)
    if kmodes is None:
        return JSONResponse(status_code=404, content={})

    return JSONResponse(status_code=200, content={
        "trace_id": kmodes.trace_id,
        "reference_id": kmodes.reference_id,
        "reference_date": kmodes.reference_date.isoformat(),
        "reference_link": kmodes.reference_link,
        "thumbnail": kmodes.thumbnail,
        "is_convert": kmodes.is_convert,
        "title": kmodes.title,
        "content": kmodes.content
    })


@kmodes_rotuer.post(path="/kmodes/{trace_id:str}/convert")
def kmodes_convert(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(KmodesUsecase)
):
    return JSONResponse(status_code=200, content=usecase.convert(trace_id=trace_id))
