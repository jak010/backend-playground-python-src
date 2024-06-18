from fastapi.routing import APIRouter

from settings.config.exception_handler import ExceptionHandlerRoute

pet_router = APIRouter(tags=['PET'], prefix='/api/v1/pet', route_class=ExceptionHandlerRoute)
pet_breed_router = APIRouter(tags=['PET'], prefix='/api/v1/pet/breeds', route_class=ExceptionHandlerRoute)
pet_attachment_router = APIRouter(tags=['PET'], prefix='/api/v1/pet', route_class=ExceptionHandlerRoute)
