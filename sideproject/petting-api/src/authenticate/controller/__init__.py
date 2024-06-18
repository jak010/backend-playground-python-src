from fastapi.routing import APIRouter

from settings.config.exception_handler import ExceptionHandlerRoute

authenticate_router = APIRouter(tags=['AUTH'], prefix='/api/v1/auth', route_class=ExceptionHandlerRoute)
kakao_oauth_router = APIRouter(tags=['OAUTH'], prefix='/api/v1/oauth/kakao', route_class=ExceptionHandlerRoute)
