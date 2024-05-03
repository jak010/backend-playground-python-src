from fastapi import Depends, Body
from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.domain.member.entity import MemberEntity, MemberProfileEntity
from src.infra.repository import MemberRepositry, MemberProfileRepository

api_router = APIRouter(tags=['RELATION'], prefix="/api/v1")
