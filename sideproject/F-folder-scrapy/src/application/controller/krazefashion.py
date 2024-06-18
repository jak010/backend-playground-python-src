from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import JSONResponse

from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.krazefashion.krazefashion_usecase import KrazeFashionUsecase

krazefashion_rotuer = APIRouter(tags=['KrazeFashion'], prefix="/api")


@krazefashion_rotuer.get(path="/krazefashion")
def krazefashion_list(
        sort_key: Literal['id', 'reference_date'] = Query(default='id'),
        sort_type: Literal['DESC', 'ASC'] = Query(default='DESC'),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10),

        usecase: USECASE_TYPE = Depends(KrazeFashionUsecase)
):
    krazefashion_contents_list, krazefashion_contents_count = usecase.get_content_list(
        page=page,
        item_per_page=item_per_page,
        sort_key=sort_key,
        sort_type=sort_type
    )

    return JSONResponse(status_code=200, content={
        "page": page,
        "item_per_page": item_per_page,
        "total_count": krazefashion_contents_count,
        "items": [{
            "trace_id": krazefashion.trace_id,
            "reference_id": krazefashion.reference_id,
            "reference_date": krazefashion.reference_date.isoformat(),
            "reference_link": krazefashion.reference_link,
            "thumbnail": krazefashion.thumbnail,
            "is_convert": krazefashion.is_convert,
            "title": str(krazefashion.title)
        } for krazefashion in krazefashion_contents_list]})


@krazefashion_rotuer.get(path="/krazefashion/{trace_id:str}")
def krazefashion_retreieve(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(KrazeFashionUsecase)
):
    krazefashion = usecase.get_content(trace_id=trace_id)
    if krazefashion is None:
        return JSONResponse(status_code=404, content={})

    return JSONResponse(status_code=200, content={
        "trace_id": krazefashion.trace_id,
        "reference_id": krazefashion.reference_id,
        "reference_date": krazefashion.reference_date.isoformat(),
        "reference_link": krazefashion.reference_link,
        "thumbnail": krazefashion.thumbnail,
        "is_convert": krazefashion.is_convert,
        "title": krazefashion.title,
        "content": krazefashion.content
    })


@krazefashion_rotuer.post(path="/krazefashion/{trace_id:str}/convert")
def krazefashion_convert(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(KrazeFashionUsecase)
):
    return JSONResponse(status_code=200, content=usecase.convert(trace_id=trace_id))
