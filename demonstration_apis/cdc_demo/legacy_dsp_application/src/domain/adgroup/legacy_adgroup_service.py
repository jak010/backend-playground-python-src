from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from fastapi.exceptions import HTTPException

from .i_legacy_adgroup_repository import ILegacyAdGroupRepository
from .legacy_adgroup import LegacyAdGroup

if TYPE_CHECKING:
    from ...apis.schema.legacy_adgroup_schema import LegacyAdGroupCreateSchema


class LegacyAdGroupCreateRequest:
    name: str
    campaign_id: int
    user_id: str
    link_url: str


class LegacyAdGroupService:
    repo = ILegacyAdGroupRepository()

    def create(self, command: LegacyAdGroupCreateSchema.LegacyAdGroupCreateRequest) -> LegacyAdGroup:
        return self.repo.save(
            LegacyAdGroup.of(
                name=command.name,
                campaign_id=command.campaign_id,
                user_id=command.user_id,
                link_url=command.link_url
            )
        )

    def find(self, adgroup_id: int) -> Optional[LegacyAdGroup]:
        return self.repo.find_by_id(pk=adgroup_id)

    def find_by_id(self, adgroup_id: int) -> Optional[LegacyAdGroup]:
        adgroup = self.repo.find_by_id(pk=adgroup_id)
        if adgroup is None:
            raise HTTPException(status_code=404, detail="adgroup not found")
        return adgroup

    def update_name(self, adgroup_id: int, name: str):
        adgroup = self.repo.find_by_id(pk=adgroup_id)
        if adgroup is None:
            raise HTTPException(status_code=404, detail="adgroup not found")
        adgroup.update_name(name=name)
        return self.repo.save(adgroup)

    def update_linked_url(self, adgroup_id: int, link_url: str):
        adgroup = self.repo.find_by_id(pk=adgroup_id)
        if adgroup is None:
            raise HTTPException(status_code=404, detail="adgroup not found")
        adgroup.update_linked_url(link_url=link_url)
        return self.repo.save(adgroup)

    def delete(self, adgroup_id):
        adgroup = self.repo.find_by_id(pk=adgroup_id)
        if adgroup is None:
            raise HTTPException(status_code=404, detail="adgroup not found")

        self.repo.save(adgroup.delete())
