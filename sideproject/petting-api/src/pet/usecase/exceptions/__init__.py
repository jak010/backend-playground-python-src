class NotExistPetEntityException(Exception):
    """ Pet을 찾을 수 없음 """


class MaxUploadImageLimitException(Exception):
    """ MaxUploadImageLimitException """


class PetUploadFileDuplicateException(Exception):
    """ PetUploadDuplicateException """


class PetUploadFileAlreadySetPrimaryException(Exception):
    """ 대표 사진으로 지정된 이미지가 존재함 """
