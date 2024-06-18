from typing import Literal

from fastapi import Depends, Form, UploadFile, File, Path
from fastapi.responses import JSONResponse

from settings.policy import file_policy
from src.authenticate.usecase import ServiceAgreementPolicyAuthenticate
from src.pet.controller.responses import s400, s404
from src.pet.usecase import PetImageUploadUseCase
from src.pet.usecase.exceptions import (
    PetUploadFileAlreadySetPrimaryException,
    NotExistPetEntityException,
    MaxUploadImageLimitException, PetUploadFileDuplicateException
)
from src.session.entity import SessionEntity
from . import pet_attachment_router


@pet_attachment_router.post(
    path="{pet_id}/attachment",
    description="강아지 단독 사진",
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "PatAttachmnetDuplicateResponse": {"value": s400.PatAttachmnetDuplicateResponse.body()},
                "PetMaxUploadImageLimit": {"value": s400.PetAttachmentMaxUploadLimitResponse.body()},
                "PetUploadFileAlreadySetPrimary": {"value": s400.PetAttachmentFileAlreadySetPrimaryResponse.body()},
                "PetUploadDuplicate": {"value": s400.PatAttachmnetDuplicateResponse.body()},
            }}}
        },
        404: {
            "content": {"application/json": {"examples": {
                "NotExistPetEntityException": {"value": s404.NotFoundPetResponse.body()},
            }}}
        }
    },
    dependencies=[
        Depends(file_policy.upload_size_policy),
        Depends(file_policy.upload_extension_policy)
    ]
)
async def pet_image_upload(
        pet_id: str = Path(),
        upload_file: UploadFile = File(...),
        attachment_label: Literal['PET', 'SELFIE'] = Form(),
        attachment_type: Literal['PRIMARY', 'SECONDARY'] = Form(),

        session: SessionEntity = Depends(ServiceAgreementPolicyAuthenticate()),
        usecase: PetImageUploadUseCase = Depends(PetImageUploadUseCase)
):
    try:
        await usecase.execute(
            owner=session,
            pet_id=pet_id,
            attachment_type=attachment_type,
            attachment_label=attachment_label,
            file=upload_file
        )
    except NotExistPetEntityException:
        return s404.NotFoundPetResponse()
    except PetUploadFileDuplicateException:
        return s400.PatAttachmnetDuplicateResponse()
    except MaxUploadImageLimitException:
        return s400.PetAttachmentMaxUploadLimitResponse()
    except PetUploadFileAlreadySetPrimaryException:
        return s400.PetAttachmentFileAlreadySetPrimaryResponse()

    return JSONResponse(status_code=200, content={})
