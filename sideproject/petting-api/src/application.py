from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from settings.config.base import ExecuteEnviorment
from settings.config.config_manager import ConfigManager
from src.authenticate.controller import kakao_oauth_router, authenticate_router
from src.certification.controller import ceritifcation_router
from src.member.controller import member_router, member_profile_router
from src.social.controller import social_router
from src.pet.controller import (
    pet_router,
    pet_breed_router,
    pet_attachment_router
)
from src.webhook.controller import webhook_router

index_router = APIRouter(tags=['INDEX'], prefix="")


@index_router.get(path="/")
def health_check():
    return JSONResponse(status_code=200, content={})


class PettingApplication(ExecuteEnviorment):
    app = FastAPI(
        title="Petting API"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def __call__(self, *args, **kwargs):
        config_manager = ConfigManager(app=self.app)

        config_manager.patch_database(db_config=self.get_database_url)
        config_manager.patch_adapter()
        config_manager.patch_orm()
        config_manager.patch_routers(
            routers=[
                index_router,
                # Authenticate
                kakao_oauth_router, authenticate_router,
                # Member
                member_router, member_profile_router,
                # Certificate
                ceritifcation_router,
                # Pet
                pet_router, pet_breed_router, pet_attachment_router,
                # Assessment
                # assessment_router

                # WebHook
                webhook_router,

                # social
                social_router

            ])

        return self.app


PettingApplication = PettingApplication()
