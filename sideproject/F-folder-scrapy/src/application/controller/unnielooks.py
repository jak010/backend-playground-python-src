from typing import Literal

from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.unnielooks.unnielooks_usecase import UnnieLooksUsecase

unnielooks_router = APIRouter(tags=['Unnielooks'], prefix="/api")


@unnielooks_router.get(path="/unnielooks")
def unnielooks_list(
        sort_key: Literal["id", "reference_date"] = Query(default='id'),
        sort_type: Literal["DESC", "ASC"] = Query(default='DESC'),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10),

        usecase: USECASE_TYPE = Depends(UnnieLooksUsecase)
):
    unnielooks_items, unnielooks_total_count = usecase.get_content_list(
        sort_key=sort_key,
        sort_type=sort_type,
        page=page,
        item_per_page=item_per_page
    )
    return JSONResponse(
        status_code=200,
        content={
            "sort_key": sort_key,
            "sorrt_type": sort_type,
            "page": page,
            "item_per_page": item_per_page,
            "total_count": unnielooks_total_count,
            "items": [{
                "id": unnielooks_item.id,
                "trace_id": unnielooks_item.trace_id,
                "reference_id": unnielooks_item.reference_id,
                "reference_date": unnielooks_item.reference_date.isoformat(),
                "reference_link": unnielooks_item.reference_link,
                "thumbnail": unnielooks_item.thumbnail,
                "is_convert": unnielooks_item.is_convert,
                "title": unnielooks_item.title
            } for unnielooks_item in unnielooks_items]
        })


@unnielooks_router.get(path="/unnielooks/{trace_id:str}")
def unnielooks_content_retreieve(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(UnnieLooksUsecase)
):
    unnielook = usecase.get_content(trace_id=trace_id)
    if unnielook is None:
        return JSONResponse(status_code=404, content={})

    return JSONResponse(
        status_code=200,
        content={
            "id": unnielook.id,
            "trace_id": unnielook.trace_id,
            "reference_id": unnielook.reference_id,
            "reference_date": unnielook.reference_date.isoformat(),
            "reference_link": unnielook.reference_link,
            "thumbnail": unnielook.thumbnail,
            "is_convert": unnielook.is_convert,
            "title": unnielook.title,
            "content": unnielook.content
        })


@unnielooks_router.post(path="/unnielooks/{trace_id:str}/convert")
def unnielooks_content_convert(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(UnnieLooksUsecase)
):
    return JSONResponse(status_code=200, content=usecase.convert(trace_id=trace_id))
