# from __future__ import annotations
#
# import requests
#
# from libs.abstract.abstract_usecase import AbstractUseCase
# from src.member.controller.request.member_register_form_dto import MemberRegisterFormDTO
# from src.member.repository import MemberRDBRepository
# from src.member.repository.exception import MemberEntityDuplicateException
# from src.member.service import MemberService
#
#
# class MemberRegisterUseCase(AbstractUseCase):
#
#     def __init__(self):
#         self.member_service = MemberService()
#
#         self.member_rdb_repository = MemberRDBRepository()
#
#     def execute(
#             self,
#             member_register_dto: MemberRegisterFormDTO
#     ):
#         # TODO 24.03.03 : Member 인증단계 고려해 로직 업데이트 필요함
#         member_entity = self.member_service.create_member(
#             name=member_register_dto.name,
#             email=member_register_dto.email,
#             phone=member_register_dto.phone,
#             channel=member_register_dto.channel.value,
#             terms_of_marketing=member_register_dto.terms_of_marketing,
#         )
#         try:
#             self.member_rdb_repository.add(member_entity)
#         except MemberEntityDuplicateException as e:
#             raise e
