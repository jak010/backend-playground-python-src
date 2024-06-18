import datetime

from src.app.domain import SessionEntity
from src.app.usecase.abstract import AbstractUseCase
from src.app.usecase.exceptions.member import DoesNotExistMember


class ProfileUpdateUseCase(AbstractUseCase):

    @classmethod
    def execute(
            cls,
            session: SessionEntity,
            name: str = None,
            description: str = None,
            age: datetime.datetime = None,
            gender: str = None,
            body_weight: int = None,
            body_height: int = None,
            country: str = None,
            address: str = None,
            instargram_url: str = None,
            facebook_url: str = None,
            twitter_url: str = None,
            profile_image: bytes = None
    ):
        member_entity = cls.member_repository.get_by_id(member_id=session.member_id)
        if member_entity is None:
            raise DoesNotExistMember()

        profile_entity = cls.profile_repository.get_by_member_id(member_id=member_entity.id)
        profile_entity = profile_entity.update(
            member_id=member_entity.id,
            description=description,
            name=name,
            age=age,
            gender=gender,
            body_weight=body_weight,
            body_height=body_height,
            country=country,
            address=address,
            instargram_url=instargram_url,
            facebook_url=facebook_url,
            twitter_url=twitter_url,
            profile_image=profile_image,
        )
        cls.profile_repository.update(profile_entity)
        return profile_entity
