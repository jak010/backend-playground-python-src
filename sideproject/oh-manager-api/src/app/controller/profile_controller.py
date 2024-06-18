import datetime
from typing import Literal

from fastapi import APIRouter, Form, Depends, UploadFile, File

from src.app.controller.responses import s200
from src.app.usecase.authenticate.jwt_authenticate import JwtAuthenticate
from src.app.usecase.profile_usecase import ProfileUpdateUseCase
from src.config.route import TransactionRoute
from src.libs.storage.member_storage import MemberStorage

profile_router = APIRouter(tags=['PROFILE'], prefix="/api/profile", route_class=TransactionRoute)


@profile_router.put(path="")
async def profile_update(
        session=Depends(JwtAuthenticate()),
        name: str = Form(default=None, description="identity"),
        description: str = Form(default=None, description="설명"),
        age: datetime.datetime = Form(default=None, description="나이"),
        gender: Literal['MAIL', 'FEMAIL'] = Form(default=None, description="성별"),
        body_weight: int = Form(default=None, description="몸무게(kg)"),
        body_height: int = Form(default=None, description="키(cm)"),
        country: str = Form(default=None, description="국적"),
        address: str = Form(default=None, description="주소"),
        instargram_url: str = Form(default=None, description="인스타그램 URL"),
        facebook_url: str = Form(default=None, description="페이스북 URL"),
        twitter_url: str = Form(default=None, description="트위터 URL"),
        profile_image: UploadFile = File(default=None, description="프로필 사진")

):
    try:
        if profile_image is not None:
            profile_image_url = MemberStorage.upload_member_profile(
                member_id=session.member_id,
                file_name=profile_image.filename,
                file_content=profile_image.file.read(),
                content_type=profile_image.content_type
            )

        else:
            profile_image_url = None
    except Exception as e:
        profile_image_url = None
    finally:
        if profile_image is not None:
            await profile_image.close()

    # TODO 24.01.19, name 중복인 경우 Exception 처리 필요함
    profile = ProfileUpdateUseCase.execute(
        session=session,
        name=name,
        description=description,
        age=age,
        gender=gender,
        body_weight=body_weight,
        body_height=body_height,
        country=country,
        address=address,
        instargram_url=instargram_url,
        facebook_url=facebook_url,
        twitter_url=twitter_url,
        profile_image=MemberStorage.get_link(profile_url=profile_image_url) if profile_image is not None else None,
    )
    return s200.Normal(
        data=profile.to_dict()
    )
