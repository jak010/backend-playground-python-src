from fastapi.routing import APIRouter

from settings.config.exception_handler import ExceptionHandlerRoute

webhook_router = APIRouter(tags=['WEBHOOK'], prefix='/payments/webhook', route_class=ExceptionHandlerRoute)
