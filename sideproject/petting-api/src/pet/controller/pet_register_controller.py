from fastapi import Depends

from libs.utils.token_utils import SessionToken
from src.authenticate.usecase import ServiceAgreementPolicyAuthenticate
from src.pet.controller import pet_router
from src.pet.controller.requests import PetRegisterRequestFormDTO
from src.pet.controller.responses import s200, s400
from src.pet.usecase.pet_register_usecase import (
    PetRegisterUseCase,
    PetRegisteredLimitException,
    PetDuplicateException
)


@pet_router.post(
    path="",
    response_model=s200.PetDto,
    responses={
        400: {
            "content": {"application/json": {"examples": {
                "PetRegisterLimitExceeded": {"value": s400.PetRegisterLimitExceededResponse.body()},
                "PetRegisterDuplicate": {"value": s400.PetRegisterDuplicateResponse.body()},
            }}}
        }
    }
)
def pet_register(
        session: SessionToken = Depends(ServiceAgreementPolicyAuthenticate()),
        request: PetRegisterRequestFormDTO = Depends(PetRegisterRequestFormDTO.as_form),
        useacse: PetRegisterUseCase = Depends(PetRegisterUseCase)
):
    try:
        saved_pet = useacse.execute(session=session, request=request)
    except PetRegisteredLimitException:
        return s400.PetRegisterLimitExceededResponse()
    except PetDuplicateException:
        return s400.PetRegisterDuplicateResponse()

    return s200.PetDto(
        nano_id=saved_pet.nanoid,
        name=saved_pet.name
    )
