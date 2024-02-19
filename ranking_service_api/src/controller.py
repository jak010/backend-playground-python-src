from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.service import RankingService

ranking_service_router = APIRouter(tags=['API'], prefix="/api/v1")


@ranking_service_router.get("/setScore")
def set_score(
        user_id: str,
        score: int,
        service: RankingService = Depends(RankingService)
):
    result = service.set_score(user_id, score)
    return JSONResponse(status_code=200, content=result)


@ranking_service_router.get("/getScore")
def get_score(
        user_id: str,
        service: RankingService = Depends(RankingService)
):
    return JSONResponse(status_code=200, content=service.get_user_ranking(user_id))


@ranking_service_router.get("/getRanks")
def get_ranks(
        service: RankingService = Depends(RankingService)
):
    return JSONResponse(status_code=200, content=service.get_toprank(limit=3))
