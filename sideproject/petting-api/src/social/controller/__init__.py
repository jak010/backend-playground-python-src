from fastapi.routing import APIRouter

from settings.config.exception_handler import ExceptionHandlerRoute

social_router = APIRouter(tags=['SOCIAL'], prefix='/api/v1/social', route_class=ExceptionHandlerRoute)
