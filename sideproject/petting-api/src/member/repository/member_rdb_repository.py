from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import exc

from libs.abstract.abstract_rdb_repository import AbstracrtRDBRepository
from src.member.entity import MemberEntity
from src.member.repository.interface.i_member_repository import IMemberRepository
from .exception import MemberEntityDuplicateException


class MemberRDBRepository(AbstracrtRDBRepository, IMemberRepository):

    def add(self, member_entity: MemberEntity) -> MemberEntity:
        try:
            self.session.add(member_entity)
            self.session.flush()
        except exc.IntegrityError as e:
            raise MemberEntityDuplicateException from e

        return member_entity

    def find_member_by_nanoid(self, nanoid: str) -> Optional[MemberEntity]:
        query = self.session.query(MemberEntity).filter(MemberEntity.nanoid == nanoid)
        query = query.one_or_none()
        if query:
            return query

    def find_member_by_email(self, email: str) -> Optional[MemberEntity]:
        query = self.session.query(MemberEntity).filter(MemberEntity.email == email)
        query = query.one_or_none()
        if query:
            return query

    def update_member_agreement(self,
                                nanoid: str,
                                terms_of_age: bool = False,
                                terms_of_agreement: bool = False,
                                terms_of_privacy: bool = False,
                                terms_of_geolocation: bool = False,
                                terms_of_marketing: bool = False
                                ):
        query = self.session.query(MemberEntity).filter(MemberEntity.nanoid == nanoid)
        query.update({
            MemberEntity.terms_of_age: terms_of_age,
            MemberEntity.terms_of_agreement: terms_of_agreement,
            MemberEntity.terms_of_privacy: terms_of_privacy,
            MemberEntity.terms_of_geolocation: terms_of_geolocation,
            MemberEntity.terms_of_marketing: terms_of_marketing
        })

    def update_member_cerification_phone(self, nanoid: str):
        self.session.query(MemberEntity).filter(MemberEntity.nanoid == nanoid).update({
            MemberEntity.certificate_of_phone: True,
            MemberEntity.certificate_of_phone_registered_at: datetime.datetime.now(),
            MemberEntity.modified_at: datetime.datetime.now()
        })

    def update_coin_quantity(self, nanoid: str, quantity: int):
        query: MemberEntity = self.session.query(MemberEntity).filter(MemberEntity.nanoid == nanoid).one()
        query.increase_coin(quantity=quantity)
        self.add(member_entity=query)
