from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import JSONResponse

from src.application.controller.type_define import USECASE_TYPE
from src.libs.resource.fashioninsight.fashioninsight_usecase import FashionInsightUsecase

fashioninsight_rotuer = APIRouter(tags=['FashionInsight'], prefix="/api")


@fashioninsight_rotuer.get(path="/fashioninsight")
def fashioninsight_list(
        sort_key: Literal['id', 'reference_date'] = Query(default='id'),
        sort_type: Literal['DESC', 'ASC'] = Query(default='DESC'),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10, ge=10, le=30),

        usecase: USECASE_TYPE = Depends(FashionInsightUsecase)
):
    fashioninsighs_contents, fashioninsighs_contents_count = usecase.get_content_list(
        sort_key=sort_key,
        sort_type=sort_type,
        page=page,
        item_per_page=item_per_page,
    )
    return JSONResponse(
        status_code=200,
        content={
            "sort_key": sort_key,
            "sort_type": sort_type,
            "page": page,
            "item_per_page": item_per_page,
            "total_count": fashioninsighs_contents_count,
            "items ": [{
                "trace_id": fashioninsight.trace_id,
                "reference_id": fashioninsight.reference_id,
                "reference_date": fashioninsight.reference_date.isoformat(),
                "reference_link": fashioninsight.reference_link,
                "thumbnail": fashioninsight.thumbnail,
                "is_convert": fashioninsight.is_convert,
                "title": fashioninsight.title
            } for fashioninsight in fashioninsighs_contents]})


@fashioninsight_rotuer.get(path="/fashioninsight/{trace_id:str}")
def fashioninsight_retreieve(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(
            FashionInsightUsecase)
):
    fashioninsight = usecase.get_content(trace_id=trace_id)
    return JSONResponse(status_code=200, content={
        "trace_id": fashioninsight.trace_id,
        "reference_id": fashioninsight.reference_id,
        "reference_date": str(fashioninsight.reference_date),
        "reference_link": fashioninsight.reference_link,
        "thumbnail": fashioninsight.thumbnail,
        "is_convert": fashioninsight.is_convert,
        "title": str(fashioninsight.title),
        "content": str(fashioninsight.content)
    })


@fashioninsight_rotuer.post(path="/fashioninsight/{trace_id:str}/convert")
def fashioninsight_convert(
        trace_id: str = Path(),
        usecase: USECASE_TYPE = Depends(FashionInsightUsecase)
):
    return JSONResponse(status_code=200, content=usecase.convert(trace_id=trace_id))
