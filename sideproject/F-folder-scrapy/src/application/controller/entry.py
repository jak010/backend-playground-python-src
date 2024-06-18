from __future__ import annotations

from fastapi import APIRouter, Form, BackgroundTasks
from fastapi.responses import JSONResponse

from src.libs.resource.eyesmag.eyesmag_usecase import EyesMagUsecase
from src.libs.resource.fashionchingu.fashionchingu_usecase import FashionChinguUsecase
from src.libs.resource.fashioninsight.fashioninsight_usecase import FashionInsightUsecase
from src.libs.resource.harpersbazaar.harpersbazaar_usecase import HarpersBazaarUsecase
from src.libs.resource.kmodes.kmodes_usecase import KmodesUsecase
from src.libs.resource.krazefashion.krazefashion_usecase import KrazeFashionUsecase
from src.libs.resource.krazemedia.krazemedia_usecase import KrazeMediaUsecase
from src.libs.resource.unnielooks.unnielooks_usecase import UnnieLooksUsecase
from src.libs.resource.voguekorea.voguekorea_usecase import VogueKoreaUsecase
from src.libs.resource.yesstyle.yesstyle_usecase import YesstyleUsecase

entry_router = APIRouter(tags=['Entry'])


@entry_router.get(path="/")
def health_check():
    return JSONResponse(status_code=200, content={})


@entry_router.get(path="/statistics")
def statistics():
    data = {
        usecase.__class__.__name__.replace("Usecase", ""): usecase.get_count()
        for usecase in [
            VogueKoreaUsecase(),
            FashionChinguUsecase(),
            FashionInsightUsecase(),
            EyesMagUsecase(),
            YesstyleUsecase(),
            HarpersBazaarUsecase(),
            KmodesUsecase(),
            KrazeFashionUsecase(),
            KrazeMediaUsecase(),
            HarpersBazaarUsecase(),
            UnnieLooksUsecase()
        ]
    }

    return JSONResponse(status_code=200, content={
        "total": sum(data.values()),
        "items": data
    })


@entry_router.post(path="/code")
async def hidden(
        background_tasks: BackgroundTasks,
        code: str = Form(description="hidden code"),
):
    if code == '76c09bc2-6c83-4449-9151-e844e0a36888':
        background_tasks.add_task(VogueKoreaUsecase().all_collect)
    if code == 'a678692b-1633-4ae6-b6bb-67590ac21aac':
        background_tasks.add_task(FashionChinguUsecase().all_collect)
    if code == '6cfdbc27-dca0-405d-ac07-df652cd63db8':
        background_tasks.add_task(EyesMagUsecase().all_collect)
    if code == '554ebafd-8df5-4c62-b10b-76fb4fc8c20e':
        background_tasks.add_task(FashionInsightUsecase().all_collect)
    if code == 'e4c065f0-ba4b-459d-88c6-cfc0bd4c7c09':
        background_tasks.add_task(YesstyleUsecase().all_collect)
    if code == '8d646cf2-c57c-436d-b1f9-8d34c4ec0bea':
        background_tasks.add_task(HarpersBazaarUsecase().all_collect)
    if code == '16fc39c7-1ce7-480e-8961-a4c4d6865b73':
        background_tasks.add_task(KmodesUsecase().all_collect)
    if code == '75f50708-1a07-40f3-9e93-770cfa1a396e':
        background_tasks.add_task(KrazeFashionUsecase().all_collect)
    if code == 'e4c065f0-1a07-b6bb-9e93-df652cd63db8':
        background_tasks.add_task(KrazeMediaUsecase().all_collect)
    if code == 'd29c6060-7795-11ee-bdef-0242ac1c000c':
        background_tasks.add_task(UnnieLooksUsecase().all_collect)

    return JSONResponse(status_code=201, content={})
