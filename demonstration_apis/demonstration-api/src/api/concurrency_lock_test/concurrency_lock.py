import time

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.domain.posts.post_repository import PostRepository
from src.domain.posts.post_entity import PostEntity, LikeIncreateLimitException

concurrency_lock_test_router = APIRouter(tags=['CONCURRENCY-OPTIMISTIC/PESSIMISTIC'], prefix='/api/v1/post')


@concurrency_lock_test_router.post(path="")
def create_post(
        repository: PostRepository = Depends(PostRepository)
):
    """ post 생성하기"""
    repository.save(
        post_entity=PostEntity.new(
            like=0,
            modified_at=int(time.time()),
            version=1
        )
    )

    return JSONResponse(status_code=200, content={})


@concurrency_lock_test_router.get(path="")
async def increase_like_post(
        repository: PostRepository = Depends(PostRepository)
):
    """ post의 like 수 증가시키기 """

    try:
        post = repository.find_by_pk(pk=1)
        # post.increase_like()
        # repository.save(post)

        # post = repository.find_by_pk(pk=1)
        # post.increase_like()

        # repository.increase_like(post_entity=post)
        is_sucess = repository.increase_like_by_optimistic_lock(post_entity=post)
        while not bool(is_sucess):
            is_sucess = repository.increase_like_by_optimistic_lock(post_entity=post)

    except LikeIncreateLimitException:
        repository.session.rollback()
        return JSONResponse(status_code=400, content={"message": "LIMIT LIKE"})

    repository.session.commit()

    return JSONResponse(status_code=200, content={})


@concurrency_lock_test_router.get(path="/v2")
async def increase_like_post_v2(
        repository: PostRepository = Depends(PostRepository)
):
    """ post의 like 수 증가시키기 (v2) """

    try:
        post = repository.find_by_pk(pk=1)
        is_sucess = repository.increase_like_by_optimistic_lock_in_mapper_args(post_entity=post)

    except LikeIncreateLimitException:
        repository.session.rollback()
        return JSONResponse(status_code=400, content={"message": "LIMIT LIKE"})

    repository.session.commit()

    return JSONResponse(status_code=200, content={})


@concurrency_lock_test_router.post(path="/reset")
def reset_post(
        repository: PostRepository = Depends(PostRepository)
):
    """ post like 초기화 """
    post = repository.find_by_pk(pk=1)
    post.reset_like()

    repository.save(post_entity=post)

    return JSONResponse(status_code=200, content={})
