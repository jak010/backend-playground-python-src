from libs.abstract.abstract_usecase import AbstractUseCase
from src.member.controller.request import RequestMemberTemsrOfAgreementsFormDTO
from src.member.repository import MemberRDBRepository
from src.session.entity import SessionEntity


class MemberServiceAggrementUpdateUseCase(AbstractUseCase):
    member_repository = MemberRDBRepository()

    def execute(
            self,
            session: SessionEntity,
            request: RequestMemberTemsrOfAgreementsFormDTO
    ):
        self.member_repository.update_member_agreement(
            nanoid=session.member_id,
            terms_of_age=request.terms_of_age,
            terms_of_agreement=request.terms_of_agreement,
            terms_of_privacy=request.terms_of_privacy,
            terms_of_geolocation=request.terms_of_geolocation,
            terms_of_marketing=request.terms_of_marketing,
        )
