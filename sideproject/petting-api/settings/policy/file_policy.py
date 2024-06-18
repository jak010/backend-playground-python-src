from fastapi import UploadFile
from fastapi.exceptions import HTTPException

from libs.utils.file_utils import bytes_to_mb

_COMMON_UPLOAD_SIZE_LIMIT = 10 * 1024 * 1024  # 10MB
_COMMON_UPLOAD_FILE_EXTENSIONS = ['image/jpeg', 'image/png']


def upload_size_policy(upload_file: UploadFile):
    if bytes_to_mb(upload_file.size) > _COMMON_UPLOAD_SIZE_LIMIT:  # 10 MB
        raise HTTPException(status_code=413, detail='File Szie exceeds limit of 10M')


def upload_extension_policy(upload_file: UploadFile):
    if upload_file.content_type not in _COMMON_UPLOAD_FILE_EXTENSIONS:
        raise HTTPException(status_code=400, detail='Not Allowed File Extenstions')
