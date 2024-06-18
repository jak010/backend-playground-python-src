from __future__ import annotations

from typing import Optional, Literal

from fastapi import APIRouter, Path, Query, Depends, Form, Request
from fastapi.responses import JSONResponse

from src.libs.resource.abstracts.abstract_usecase import AbstractUsecaseCRUDImplements
from src.libs.resource.post.post_entity import PostEntity
from src.libs.resource.post.post_usecase import PostUsecase

post_router = APIRouter(tags=['Posts'], prefix="/api")

SEARCHABLE_PLATFORM = Literal[
    'voguekorea',
    'fashionchingu',
    'fashioninsight',
    'eyesmag',
    'harpersbazaar',
    'kmodes',
    'krazefashion',
    'krazemedia',
    'unnielooks',
    'yesstyle',
]


@post_router.get(path="/posts", description="LLM Contents 목록조회")
def post_content_list(
        platform: SEARCHABLE_PLATFORM = Query(default=None),
        keyword: Optional[str] = Query(default=None),
        content: Optional[str] = Query(default=None),

        page: int = Query(default=1, ge=1),
        item_per_page: int = Query(default=10, ge=10, le=30),
        sort_key: Literal['views', 'created_at'] = Query(default="created_at"),
        sort_type: Literal['DESC', 'ASC'] = Query(default="DESC"),

        usecase: AbstractUsecaseCRUDImplements[PostEntity] = Depends(PostUsecase)
):
    posts, posts_count = usecase.get_content_list(
        keyword=keyword,
        platform=platform,
        content=content,
        page=page,
        item_per_page=item_per_page,
        sort_key=sort_key,
        sort_type=sort_type
    )

    return JSONResponse(
        status_code=200,
        content={
            "total_count": posts_count,
            "items": [{
                "post_id": post.post_id,
                "trace_id": post.trace_id,
                "keyword": post.keyword,
                "platform": post.platform,
                "title": post.title,
                "content": post.content,
                "thumbnail": post.thumbnail,
                "reference_link": post.reference_link,
                "views": post.views,
                "is_deleted": post.is_deleted,
                "created_at": post.created_at,
                "modified_at": post.modified_at,
            } for post in posts]
        })


@post_router.get(path="/posts/today", description="오늘 생성된 콘텐츠")
def post_created_content_today(usecase: PostUsecase = Depends(PostUsecase)):
    return JSONResponse(
        status_code=200,
        content={
            'count': usecase.get_created_today_content()
        }
    )


@post_router.get(path="/posts/{trace_id:str}", description="LLM Contents 상세")
def post_contenet_retreieve(
        request: Request,
        trace_id: str = Path(),
        usecase: AbstractUsecaseCRUDImplements[PostEntity] = Depends(PostUsecase)
):
    post = usecase.get_content(trace_id=trace_id, request=request)
    if post is None:
        return JSONResponse(status_code=404, content={})

    return JSONResponse(
        status_code=200,
        content={
            "post_id": post.post_id,
            "keyword": post.keyword,
            "platform": post.platform,
            "title": post.title,
            "content": post.content,
            "thumbnail": post.thumbnail,
            "reference_link": post.reference_link,
            "views": post.views,
            "is_deleted": post.is_deleted,
            "created_at": post.created_at,
            "modified_at": post.modified_at
        })


@post_router.put(path="/posts/{trace_id:str}", description="LLM Contents 수정")
def post_content_update(
        trace_id: str = Path(),
        title: Optional[str] = Form(default=None),
        content: Optional[str] = Form(default=None),
        keyword: Optional[str] = Form(default=None),
        is_deleted: Optional[int] = Form(default=None, ge=0, le=1),  # 0: 게시, 1: 게시x

        usecase: AbstractUsecaseCRUDImplements = Depends(PostUsecase)
):
    usecase.update_by(
        trace_id=trace_id,
        title=title,
        content=content,
        keyword=keyword,
        is_deleted=is_deleted
    )

    return JSONResponse(
        status_code=201,
        content={}
    )
