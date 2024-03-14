from __future__ import annotations

from src.domain.entity.abstract import AbstractEntity, generate_entity_id

from src.domain.value_object.address import Address


class MemberEntity(AbstractEntity):
    root_entity: MemberEntity

    nanoid: str
    name: str
    age: int
    address: Address

    @staticmethod
    def new(name: str, age: int, address: Address = None):
        _entity = MemberEntity(
            nanoid=generate_entity_id(),
            name=name,
            age=age,
            address=address
        )
        _entity.address = address

        return _entity

    def change_address(self, address: Address):
        self.address = address
