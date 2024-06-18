from __future__ import annotations

from libs.abstract.abstract_rdb_repository import AbstracrtRDBRepository as _AbstracrtRDBRepository
from src.member.entity import MemberAssetEntity
from src.member.enums import MemberAssetType


class MemberAssetRDBRepository(_AbstracrtRDBRepository):

    @classmethod
    def add(cls, entity: MemberAssetEntity):
        cls.session.add(entity)
        return entity

    def find_member_asset_by_coin_type(self, member_id: str) -> MemberAssetEntity:
        query: MemberAssetEntity = self.session.query(MemberAssetEntity) \
            .filter(MemberAssetEntity.nanoid == member_id) \
            .filter(MemberAssetEntity.type == MemberAssetType.COIN.value) \
            .one_or_none()
        return query

    def find_member_asset_by_image_upload_event(self, member_id: str, reason: str) -> MemberAssetEntity:
        query: MemberAssetEntity = self.session.query(MemberAssetEntity) \
            .filter(MemberAssetEntity.nanoid == member_id) \
            .filter(MemberAssetEntity.type == MemberAssetType.COIN.value) \
            .filter(MemberAssetEntity.reason == reason) \
            .one_or_none()
        return query
