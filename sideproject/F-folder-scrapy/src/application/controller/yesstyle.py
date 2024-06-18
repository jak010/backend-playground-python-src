from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse

from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.yesstyle.yesstyle_usecase import YesstyleUsecase

yesstyle_rotuer = APIRouter(tags=['Yesstyle'], prefix="/api")


@yesstyle_rotuer.get(path="/yesstyle")
def yesstyle_list(
        sort_key: Literal['id', 'reference_date'] = Query(default='id'),
        sort_type: Literal['DESC', 'ASC'] = Query(default='DESC'),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10, ge=10, le=30),

        usecase: USECASE_TYPE = Depends(YesstyleUsecase)
):
    yesstyle_conetents, yesstyle_conetents_count = usecase.get_content_list(
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
            "total_count": yesstyle_conetents_count,
            "items ": [{
                "trace_id": yesstyle.trace_id,
                "reference_id": yesstyle.reference_id,
                "reference_date": yesstyle.reference_date.isoformat(),
                "reference_link": yesstyle.reference_link,
                "thumbnail": yesstyle.thumbnail,
                "is_convert": yesstyle.is_convert,
                "title": yesstyle.title
            } for yesstyle in yesstyle_conetents]})


@yesstyle_rotuer.get(path="/yesstyle/{trace_id:str}")
def yesstyle_retreieve(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(YesstyleUsecase)
):
    yesstyle_conetent = usecase.get_content(trace_id=trace_id)
    if yesstyle_conetent is None:
        return JSONResponse(status_code=404, content={})

    return JSONResponse(status_code=200, content={
        "id": yesstyle_conetent.id,
        "trace_id": yesstyle_conetent.trace_id,
        "reference_id": yesstyle_conetent.reference_id,
        "reference_date": str(yesstyle_conetent.reference_date),
        "reference_link": yesstyle_conetent.reference_link,
        "thumbnail": yesstyle_conetent.thumbnail,
        "is_convert": yesstyle_conetent.is_convert,
        "title": yesstyle_conetent.title,
        "content": yesstyle_conetent.content
    })


@yesstyle_rotuer.post(path="/yesstyle/{trace_id:str}/convert")
def yesstyle_content_convert(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(YesstyleUsecase)
):
    yesstyle_conetent = usecase.convert(trace_id=trace_id)
    if yesstyle_conetent is None:
        return JSONResponse(status_code=404, content={})

    return JSONResponse(status_code=200, content=yesstyle_conetent)
