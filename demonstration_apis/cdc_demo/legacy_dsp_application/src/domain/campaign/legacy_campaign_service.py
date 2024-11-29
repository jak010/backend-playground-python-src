from .i_legacy_campaign_repository import ILegacyCampaignRepository

from .legacy_campaign import LegacyCampaign


class LegacyCampignService:
    repo = ILegacyCampaignRepository()

    def create(self, name: str, user_id: int, budget: int) -> LegacyCampaign:
        return self.repo.save(
            model=LegacyCampaign.of(
                name=name, user_id=user_id, budget=budget
            )
        )

    def find_by_id(self, campaign_id: int):
        return self.repo.find_by_id(pk=campaign_id)
