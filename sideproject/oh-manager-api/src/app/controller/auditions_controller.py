from fastapi import APIRouter, Depends, Query

from src.app.controller.responses import s200

from src.app.domain.session.session_entity import SessionEntity
from src.app.usecase.audition_usecase import ReadAuditionListUseCase
from src.app.usecase.authenticate.jwt_authenticate import JwtAuthenticate
from src.config.route import TransactionRoute
from src.app.controller.swagger.response_model import (
    ResponseEntityModel,
    AUDITIONS_ENTITY_MODEL
)

auditions_router = APIRouter(tags=['AUDITION'], prefix="/api/auditions", route_class=TransactionRoute)


@auditions_router.get(
    path="",
)
def auditons_list(
        session: SessionEntity = Depends(JwtAuthenticate()),
        page: int = Query(default=1),
        item_per_page: int = Query(default=10)
) -> ResponseEntityModel[AUDITIONS_ENTITY_MODEL]:
    auditions_list = ReadAuditionListUseCase.execute(
        session=session,
        page=page,
        item_per_page=item_per_page
    )

    data = []
    if auditions_list:
        data = [
            auditions.read(
                exclude_fields=["uid", "author", "platform", "link", "created_at", "modified_at"]
            ) for auditions in auditions_list
        ]

    return s200.Normal(data={
        "items": data
    })
