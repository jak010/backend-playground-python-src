from datetime import datetime

from fastapi.exceptions import HTTPException

from .i_legacy_keyword_repository import ILegacyKeywordRepository

from .legacy_keyword import LegacyKeyword


class LegacyKeywordService:
    repo = ILegacyKeywordRepository()

    def create(self, text: str, adgroup_id: int, user_id: str) -> LegacyKeyword:
        return self.repo.save(
            model=LegacyKeyword.of(
                text=text, adgroup_id=adgroup_id, user_id=user_id
            )
        )

    def find_by_id(self, campaign_id: int):
        return self.repo.find_by_id(pk=campaign_id)

    def find(self):
        return self.repo.find()

    def delete(self, pk: int) -> LegacyKeyword:
        """ 유저 삭제하기 (soft delete) """
        legacy_keyword = self.repo.find_by_id(pk=pk)
        if legacy_keyword is None:
            raise HTTPException(status_code=404, detail="legacy keyword not found")

        try:
            delete_legacy_keyword = legacy_keyword.delete()
        except Exception:
            raise HTTPException(status_code=400, detail="legacy keyword already delete")

        return self.repo.save(delete_legacy_keyword)
