from fastapi.routing import APIRouter

from settings.config.exception_handler import ExceptionHandlerRoute

member_router = APIRouter(tags=['MEMBER'], prefix='/api/v1/member', route_class=ExceptionHandlerRoute)
member_profile_router = APIRouter(tags=['MEMBER'], prefix='/api/v1/member/profile', route_class=ExceptionHandlerRoute)
