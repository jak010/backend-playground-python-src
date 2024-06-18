from adapter.kakao.resource.abstract import AbstractKaKaoResource
from .dto.kakao_local_search_address_dto import KaKaoLocalSearchAddressDto

# from .kakao_oidc_user_info import KaKaoOIDCUserInfo
from .kakao_local_search_address import KaKaoLocalSearchAddress


class KaKaoGeoResourceEntry(AbstractKaKaoResource):

    def get_local_search(self, address: str) -> KaKaoLocalSearchAddressDto:
        data = KaKaoLocalSearchAddress.get_user_info(client_id=self.config.client_id, address=address)

        return KaKaoLocalSearchAddressDto.from_dict(data)
