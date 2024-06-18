from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import desc

from libs.abstract.abstract_rdb_repository import AbstracrtRDBRepository as _AbstracrtRDBRepository
from src.certification.entity import CeritifcationEntity
from src.certification.repository.interface.i_cerification_repository import ICerificationRepository


class CerificationRDBRepository(_AbstracrtRDBRepository, ICerificationRepository):

    def add(self, cerification_entity: CeritifcationEntity) -> CeritifcationEntity:
        self.session.add(cerification_entity)
        return cerification_entity

    def find_by_nanoid(self, nanoid: str) -> Optional[CeritifcationEntity]:
        query = self.session.query(CeritifcationEntity).filter(CeritifcationEntity.nanoid == nanoid).one_or_none()
        if query:
            return query

    def find_sms_cerification_in_request_with_member(self, member_id: str) -> Optional[CeritifcationEntity]:

        query = self.session.query(CeritifcationEntity) \
            .filter(CeritifcationEntity.member_id == member_id) \
            .filter(CeritifcationEntity.type == 'SMS') \
            .filter(CeritifcationEntity.status == 'REQUEST') \
            .order_by(desc(CeritifcationEntity.created_at)) \
            .one_or_none()

        if query:
            return query

    def find_sms_certification_code_with_member(self, member_id: str, code: str) -> Optional[CeritifcationEntity]:

        query = self.session.query(CeritifcationEntity) \
            .filter(CeritifcationEntity.member_id == member_id) \
            .filter(CeritifcationEntity.code == code) \
            .filter(CeritifcationEntity.type == 'SMS') \
            .filter(CeritifcationEntity.status == 'REQUEST') \
            .order_by(desc(CeritifcationEntity.created_at)) \
            .one_or_none()

        if query:
            return query

    def update_complete_sms_certification(self, member_id: str, code: str) -> Optional[CeritifcationEntity]:
        self.session.query(CeritifcationEntity) \
            .filter(CeritifcationEntity.member_id == member_id) \
            .filter(CeritifcationEntity.code == code) \
            .filter(CeritifcationEntity.type == 'SMS') \
            .filter(CeritifcationEntity.status == 'REQUEST') \
            .update(
            {
                CeritifcationEntity.status: 'COMPLETE',
                CeritifcationEntity.modified_at: datetime.datetime.now(),
            })

    def find_sms_cerification_complete(self, member_id) -> Optional[CeritifcationEntity]:
        query = self.session.query(CeritifcationEntity) \
            .filter(CeritifcationEntity.member_id == member_id) \
            .filter(CeritifcationEntity.status == 'COMPLETE') \
            .one_or_none()

        if query:
            return query
