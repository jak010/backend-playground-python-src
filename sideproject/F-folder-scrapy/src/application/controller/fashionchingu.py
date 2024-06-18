from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse

from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.fashionchingu.fashionchingu_usecase import FashionChinguUsecase

fashionchingu_rotuer = APIRouter(tags=['FashionChingu'], prefix="/api")


@fashionchingu_rotuer.get(path="/fashionchingu")
def fashionchingu_list(
        sort_key: Literal['id', 'reference_date'] = Query(default='id'),
        sort_type: Literal['DESC', 'ASC'] = Query(default='DESC'),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10, ge=10, le=30),

        usecase: USECASE_TYPE = Depends(FashionChinguUsecase)
):
    fashionchingu_contents, fashionchingu_contents_count = usecase.get_content_list(
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
            "total_count": fashionchingu_contents_count,
            "items": [{
                "id": fashionchingu_content.id,
                "trace_id": fashionchingu_content.trace_id,
                "reference_id": fashionchingu_content.reference_id,
                "reference_date": fashionchingu_content.reference_date.isoformat(),
                "reference_link": fashionchingu_content.reference_link,
                "thumbnail": fashionchingu_content.thumbnail,
                "is_convert": fashionchingu_content.is_convert,
                "title": fashionchingu_content.title
            } for fashionchingu_content in fashionchingu_contents]})


@fashionchingu_rotuer.get(path="/fashionchingu/{trace_id:str}")
def fashionchingu_content_retreieve(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(FashionChinguUsecase)
):
    fashionchingu = usecase.get_content(trace_id=trace_id)
    if fashionchingu is None:
        return JSONResponse(status_code=404, content={"msg": "Not Exist Content"})

    return JSONResponse(
        status_code=200,
        content={
            "id": fashionchingu.id,
            "trace_id": fashionchingu.trace_id,
            "reference_id": fashionchingu.reference_id,
            "reference_date": str(fashionchingu.reference_date),
            "reference_link": fashionchingu.reference_link,
            "thumbnail": fashionchingu.thumbnail,
            "is_convert": fashionchingu.is_convert,
            "title": fashionchingu.title,
            "content": fashionchingu.content
        })


@fashionchingu_rotuer.post(path="/fashionchingu/{trace_id:str}/convert")
def fashionchingu_content_convert(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(FashionChinguUsecase)
):
    return JSONResponse(status_code=200, content=usecase.convert(trace_id=trace_id))
