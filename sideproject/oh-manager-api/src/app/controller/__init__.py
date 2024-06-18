from .member_controller import member_router
from .signup_controller import signup_router
from .profile_controller import profile_router
from .session_controller import session_router
from .auditions_controller import auditions_router
from .submission_controller import submission_router

from fastapi import APIRouter
from fastapi.responses import JSONResponse

health_router = APIRouter(tags=[""], prefix="")


@health_router.get("/")
def health_check():
    return JSONResponse(content={})
