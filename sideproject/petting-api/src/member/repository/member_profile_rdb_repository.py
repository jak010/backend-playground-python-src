from __future__ import annotations

import datetime

from libs.abstract.abstract_rdb_repository import AbstracrtRDBRepository as _AbstracrtRDBRepository
from src.member.entity import MemberProfileEntity
from src.member.repository.interface import IMemberProfileRepository
from .exception import MemberProfileDuplicateException


class MemberProfileRDBRepository(_AbstracrtRDBRepository, IMemberProfileRepository):
    def add(self, member_profile_entity: MemberProfileEntity) -> MemberProfileEntity:
        query = self.session.query(MemberProfileEntity) \
            .filter(MemberProfileEntity.nanoid == member_profile_entity.nanoid) \
            .one_or_none()
        if query:
            raise MemberProfileDuplicateException()

        self.session.add(member_profile_entity)
        return member_profile_entity

    def find_member_profile_by_nanoid(self, nanoid: str) -> MemberProfileEntity:
        query = self.session.query(MemberProfileEntity) \
            .filter(MemberProfileEntity.nanoid == nanoid) \
            .one_or_none()
        if query:
            return query

    def update_profile(
            self,
            member_id: str,
            nickname: str,
            address: str,

            region1: str,
            region2: str,
            region3: str,
            road_name: str,

            latitude: float,
            longitude: float,
            description: str,
            job: str,
            birthday: datetime.datetime,
            gender: str,
            mbti: str,
    ):
        query = self.session.query(MemberProfileEntity).filter(MemberProfileEntity.nanoid == member_id)
        update_kwargs = {}

        if nickname is not None:
            update_kwargs[MemberProfileEntity.nickname] = nickname
        if address is not None:
            update_kwargs[MemberProfileEntity.address] = address
            update_kwargs[MemberProfileEntity.region1] = region1
            update_kwargs[MemberProfileEntity.region2] = region2
            update_kwargs[MemberProfileEntity.region3] = region3
            update_kwargs[MemberProfileEntity.road_name] = road_name
            update_kwargs[MemberProfileEntity.latitude] = latitude
            update_kwargs[MemberProfileEntity.longitude] = longitude
        if description is not None:
            update_kwargs[MemberProfileEntity.description] = description
        if job is not None:
            update_kwargs[MemberProfileEntity.job] = job
        if birthday is not None:
            update_kwargs[MemberProfileEntity.birthday] = birthday
        if gender is not None:
            update_kwargs[MemberProfileEntity.gender] = gender
        if mbti is not None:
            update_kwargs[MemberProfileEntity.mbti] = mbti
        update_kwargs[MemberProfileEntity.modified_at] = datetime.datetime.now()

        query.update(update_kwargs)
