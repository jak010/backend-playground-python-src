from fastapi import APIRouter

from settings.config.exception_handler import ExceptionHandlerRoute

ceritifcation_router = APIRouter(tags=['CERTIFICATE'], prefix='/api/v1/certification',
                                 route_class=ExceptionHandlerRoute)
