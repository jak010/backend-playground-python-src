import dataclasses


@dataclasses.dataclass
class KaKaoConfig:
    """ KaKao API 호출에 필요한 dataclass """
    client_id: str
    client_secret: str
    redirect_uri: str
