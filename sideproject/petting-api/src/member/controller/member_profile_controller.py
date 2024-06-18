from typing import Union

from fastapi import Depends
from fastapi.responses import JSONResponse

from src.authenticate.usecase import JwtAuthenticate
from src.authenticate.usecase import (
    ServiceAgreementPolicyAuthenticate
)
from src.member.controller.request import MemberProfileUpdateFormDTO
from src.member.controller.response import s200
from src.member.usecase import MemberProfileUpdateUseCase
from src.member.usecase import MemberReadUseCase
from src.session.entity import SessionEntity
from . import member_profile_router


@member_profile_router.get(
    path="",
    description="Member Info API, 약관 동의시 (MemberInfoModel), 약관 미동의시(MemberTersmInfoModel)",
)
def read_member_profile(
        session: SessionEntity = Depends(JwtAuthenticate()),
        usecase: MemberReadUseCase = Depends(MemberReadUseCase)
        # ) -> Union[s200.MemberTermsInfoDTO, s200.MemberInfoDTO]:  # XXX: Swagger 문서 상, Response별 example이 나타나지 않음
):
    data = usecase.execute(session=session)

    member = data["member"]
    member_profile = data["member_profile"]
    pet = data["pet"]
    pet_attachment = data["pet_attachment"]

    if not member.terms_of_agreement:
        return s200.MemberTermsInfoDTO(
            nanoid=member.nanoid,
            name=member.name,

            certificate_of_phone=member.certificate_of_phone,
            certificate_of_phone_registered_at=member.certificate_of_phone_registered_at,

            terms_of_age=member.terms_of_age,
            terms_of_agreement=member.terms_of_agreement,
            terms_of_privacy=member.terms_of_privacy,
            terms_of_geolocation=member.terms_of_geolocation,
            terms_of_marketing=member.terms_of_marketing,
        )
    else:
        return s200.MemberInfoDTO(
            nanoid=member.nanoid,
            name=member.name,
            email=member.email,
            channel=member.channel,
            phone=member.phone,
            certificate_of_phone=bool(member.certificate_of_phone),
            certificate_of_phone_registered_at=member.certificate_of_phone_registered_at,
            terms_of_age=member.terms_of_age,
            terms_of_agreement=member.terms_of_agreement,
            terms_of_privacy=member.terms_of_privacy,
            terms_of_geolocation=member.terms_of_geolocation,
            terms_of_marketing=member.terms_of_marketing,
            created_at=member.created_at,
            pet=pet,
            pet_attachment=pet_attachment,

            nickname=member_profile.nickname,
            birthday=member_profile.birthday,
            gender=member_profile.gender,
            mbti=member_profile.mbti
        )


@member_profile_router.put(path="")
def update_member_profile(
        session: SessionEntity = Depends(ServiceAgreementPolicyAuthenticate()),
        request: MemberProfileUpdateFormDTO = Depends(MemberProfileUpdateFormDTO.as_form),
        usecase: MemberProfileUpdateUseCase = Depends(MemberProfileUpdateUseCase)

):
    usecase.execute(session=session, request=request)
    return JSONResponse(status_code=200, content={})
