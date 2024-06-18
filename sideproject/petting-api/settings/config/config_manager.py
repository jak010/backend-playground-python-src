from typing import NoReturn

from fastapi import FastAPI
from sqlalchemy.orm import registry, relationship

from settings.config.base import (
    ExecuteEnviorment,
    KaKaoConfig,
    AWSConfig,
    AligoConfig
)
from settings.container.adapter_container import (
    KaKaoAdapterContainer,
    AWSAdapterContainer,
    AligoAdapterContainer
)
from settings.container.db_container import DataBaseContainer
from settings.container.event_container import EventContainer


class ConfigManager:

    def __init__(self, app: FastAPI):
        self.app = app

    def patch_routers(self, routers):
        for router in routers:
            self.app.include_router(router)

    def patch_database(self, db_config):
        db_container = DataBaseContainer(db_url=db_config)
        db_container.wire()

    def patch_adapter(self) -> NoReturn:
        """ adapter ioc initialized """
        kakao_container = KaKaoAdapterContainer(
            client_id=KaKaoConfig.CLIENT_ID.value,
            client_secret=KaKaoConfig.CLIENT_SECRET.value,
            redirect_uri=KaKaoConfig.REDIRECT_URL.value
        )
        kakao_container.wire()

        aws_container = AWSAdapterContainer(
            aws_access_key=AWSConfig.AWS_ACCESS_KEY.value,
            aws_access_secret_key=AWSConfig.AWS_ACCESS_SECRET_KEY.value,
            aws_region_name=AWSConfig.AWS_REGION_NAME.value,
            aws_s3_bucket=AWSConfig.AWS_S3_BUCKET.value,
        )
        aws_container.wire()

        aligo_container = AligoAdapterContainer(
            mode=ExecuteEnviorment.MODE,
            aligo_api_key=AligoConfig.ALIGO_API_KEY.value,
            aligo_user_id=AligoConfig.ALIGO_USER_ID.value,
            aligo_sender=AligoConfig.ALIGO_SENDER.value,
        )
        aligo_container.wire()

        event_container = EventContainer()
        event_container.wire()

    def patch_orm(self):
        """
            Domain Entity와 DataBase Table 간 Mapping 설정
        """
        from adapter.database import orm
        from src.member.entity import (
            MemberEntity,
            MemberProfileEntity,
            MemberAssetEntity
        )
        from src.session.entity import SessionEntity
        from src.certification.entity import CeritifcationEntity
        from src.pet.entity import (
            PetEntity,
            PetAttachmentEntity
        )
        from src.assessment.entity import AssessmentEntity
        from src.social.entity import SocialEntity

        orm_mapper = registry(orm.metadata)
        orm_mapper.map_imperatively(MemberEntity, orm.Member)
        orm_mapper.map_imperatively(MemberAssetEntity, orm.MemberAsset)
        orm_mapper.map_imperatively(MemberProfileEntity, orm.MemberProfile)
        orm_mapper.map_imperatively(
            SessionEntity, orm.Session,
            properties={
                'member': relationship(
                    MemberEntity,
                    primaryjoin='foreign(session.c.member_id) == member.c.nanoid',
                    lazy='joined',
                    uselist=False
                )
            }
        )
        orm_mapper.map_imperatively(CeritifcationEntity, orm.Certification)
        orm_mapper.map_imperatively(PetEntity, orm.Pet)
        orm_mapper.map_imperatively(PetAttachmentEntity, orm.PetAttachment)
        orm_mapper.map_imperatively(AssessmentEntity, orm.Assessment)
        orm_mapper.map_imperatively(SocialEntity, orm.Social)

        return orm_mapper
