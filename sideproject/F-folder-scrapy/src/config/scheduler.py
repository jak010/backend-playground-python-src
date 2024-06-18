from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from src.libs.resource.eyesmag.eyesmag_usecase import EyesMagUsecase
from src.libs.resource.fashionchingu.fashionchingu_usecase import FashionChinguUsecase
from src.libs.resource.fashioninsight.fashioninsight_usecase import FashionInsightUsecase
from src.libs.resource.harpersbazaar.harpersbazaar_usecase import HarpersBazaarUsecase
from src.libs.resource.kmodes.kmodes_usecase import KmodesUsecase
from src.libs.resource.krazefashion.krazefashion_usecase import KrazeFashionUsecase
from src.libs.resource.unnielooks.unnielooks_usecase import UnnieLooksUsecase
from src.libs.resource.voguekorea.voguekorea_usecase import VogueKoreaUsecase
from src.libs.resource.yesstyle.yesstyle_usecase import YesstyleUsecase


def periodic() -> BackgroundScheduler:
    background_scheduler = BackgroundScheduler(timezone='Asia/Seoul', daemon=True)
    background_scheduler.add_job(
        VogueKoreaUsecase().daily_collect, "cron",
        id='1', day_of_week="*", hour=13, minute=0, second=0
    )
    background_scheduler.add_job(
        FashionChinguUsecase().daily_collect, "cron",
        id='2', day_of_week="*", hour=13, minute=10, second=0
    )
    background_scheduler.add_job(
        EyesMagUsecase().daily_collect, "cron",
        id='3', day_of_week="*", hour=13, minute=20, second=0
    )
    background_scheduler.add_job(
        FashionInsightUsecase().daily_collect, "cron",
        id='4', day_of_week="*", hour=13, minute=30, second=0
    )
    background_scheduler.add_job(
        YesstyleUsecase().daily_collect, "cron",
        id='5', day_of_week="*", hour=13, minute=40, second=0
    )
    background_scheduler.add_job(
        HarpersBazaarUsecase().daily_collect, "cron",
        id='6', day_of_week="*", hour=13, minute=50, second=0
    )
    background_scheduler.add_job(
        KmodesUsecase().daily_collect, "cron",
        id='7', day_of_week="*", hour=14, minute=0, second=0
    )
    background_scheduler.add_job(
        KrazeFashionUsecase().daily_collect, "cron",
        id='8', day_of_week="*", hour=14, minute=10, second=0
    )
    background_scheduler.add_job(
        UnnieLooksUsecase().daily_collect, "cron",
        id='10', day_of_week="*", hour=14, minute=20, second=0
    )

    return background_scheduler
