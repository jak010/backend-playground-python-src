from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.domain.posts.post_repository import PostRepository
from src.domain.posts.post_entity import PostEntity, LikeIncreateLimitException

redis_lock_test_router = APIRouter(tags=['REDIS_LOCK'], prefix='/api/v1/post')


@redis_lock_test_router.post(path="")
def create_post(
        repository: PostRepository = Depends(PostRepository)
):
    """ post 생성하기"""
    repository.save(
        post_entity=PostEntity.new(
            like=0
        )
    )

    return JSONResponse(status_code=200, content={})


@redis_lock_test_router.get(path="")
async def increase_like_post(
        repository: PostRepository = Depends(PostRepository)
):
    """ post의 like 수 증가시키기 """

    try:
        post = repository.find_by_pk(pk=1)
        post.increase_like()
        repository.save(post)
    except LikeIncreateLimitException:
        return JSONResponse(status_code=200, content={"message": "LIMIT LIKE"})

    return JSONResponse(status_code=200, content={})


@redis_lock_test_router.post(path="/reset")
def reset_post(
        repository: PostRepository = Depends(PostRepository)
):
    """ post like 초기화 """
    post = repository.find_by_pk(pk=1)
    post.reset_like()

    repository.save(post_entity=post)

    return JSONResponse(status_code=200, content={})
