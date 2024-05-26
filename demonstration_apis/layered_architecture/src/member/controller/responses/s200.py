from library.http.success import PaginateReponse, BaseSuccessResponse


class MemberResponse(BaseSuccessResponse):
    STATUS_CODE = 200


class MemberPaginateResponse(PaginateReponse):
    STATUS_CODE = 200
