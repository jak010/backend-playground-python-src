from src.app.domain.abstract import AbstractRepository
from src.app.domain.profile import ProfileEntity


class ProfileRepository(AbstractRepository[ProfileEntity]):

    def add(self, profile_entity: ProfileEntity):
        self.session.add(profile_entity)
        return profile_entity

    def update(self, profile_entity: ProfileEntity):
        self.session.query(ProfileEntity) \
            .filter(ProfileEntity.member_id == profile_entity.member_id) \
            .update(profile_entity.to_dict())
        return profile_entity

    def get_by_member_id(self, *, member_id: str) -> ProfileEntity:
        query = self.session.query(ProfileEntity).filter(ProfileEntity.member_id == member_id)
        query = query.one_or_none()
        if query:
            return query
