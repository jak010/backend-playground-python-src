from fastapi import Body, Path
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LegacyAdGroup(BaseModel):
    id: Optional[int]
    name: str
    campaign_id: int
    user_id: int
    link_url: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class LegacyAdGroupCreateSchema:
    class LegacyAdGroupCreateRequest(BaseModel):
        name: str
        campaign_id: int
        user_id: int
        link_url: str

    class LegacyAdGroupResponse(LegacyAdGroup): ...


class LegacyAdGroupUpdateSchema:
    class LegacyAdGroupUpdateNameRequest(BaseModel):
        adgroup_id: int
        name: str

        @classmethod
        def as_body(cls,
                    adgroup_id: int = Path(),
                    name=Body(description="adgroup name", embed=True)
                    ):
            return cls(
                adgroup_id=adgroup_id,
                name=name
            )

    class LegacyAdGroupUpdateLinkUrlRequest(BaseModel):
        adgroup_id: int
        link_url: str

        @classmethod
        def as_body(cls,
                    adgroup_id: int = Path(),
                    link_url=Body(description="adgroup name", embed=True)
                    ):
            return cls(
                adgroup_id=adgroup_id,
                link_url=link_url
            )
