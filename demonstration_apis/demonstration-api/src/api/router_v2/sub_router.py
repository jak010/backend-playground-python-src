from fastapi.responses import JSONResponse
from fastapi import Depends

from settings.abstracts import IRepository
from .index_router import index_router_v1

from src.domain.member.repository import MemberRepository
from src.domain.posts.post_repository import PostRepository
from src.domain.member.entity import MemberEntity


@index_router_v1.get(path="/sub")
def some_router(
        repository: MemberRepository = Depends(MemberRepository)
        # repository: PostRepository = Depends(PostRepository)
):
    # print(repository.find_by_id())
    print(repository.add())
    return JSONResponse(status_code=200, content={})
