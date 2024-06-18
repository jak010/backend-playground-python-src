from src.member.entity import MemberAssetEntity
from src.member.repository import MemberAssetRDBRepository, MemberRDBRepository
from src.member.enums import MemberAssetType


class MemberAssetService:
    member_asset_repository = MemberAssetRDBRepository()

    member_repository = MemberRDBRepository()

    def issued_coin(self, quantiy, reason, member_id: str):
        member_asset = self.member_asset_repository.find_member_asset_by_coin_type(
            member_id=member_id
        )
        if member_asset is None:
            member_asset = MemberAssetEntity.new(
                member_id=member_id,
                issued_quantity=quantiy,
                reason=reason,
                type=MemberAssetType.COIN
            )
            self.member_asset_repository.add(member_asset)
            return member_asset
        else:
            member_asset.increase_quantity(quantity=quantiy)
            self.member_asset_repository.add(member_asset)
