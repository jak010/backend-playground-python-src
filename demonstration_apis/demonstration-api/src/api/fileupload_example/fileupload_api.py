from typing import List, Annotated, Optional, Union

from fastapi import APIRouter, UploadFile, Depends, File, Request, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

fileupload_router = APIRouter(tags=['FILE_UPLOAD_OBJECT'], prefix='/api/v1', redirect_slashes=False)


class FileRequestForm(BaseModel):
    upload_files: Optional[UploadFile]

    @classmethod
    # def as_form(cls, *, upload_files: List[UploadFile] = File(default=None)):
    def as_form(cls, *, upload_files: list[UploadFile] = File(None)):
        return cls(
            upload_files=upload_files
        )

    @field_validator("upload_files", mode='before')
    def validator_upload_files(cls, upload_files: List[UploadFile]):
        return upload_files


# @fileupload_router.post(path="")
# def file_uploads(
#         # upload_files: List[UploadFile] = Form(default=None)
#         request: FileRequestForm = Depends(FileRequestForm.as_form)
# ):
#     """ post 생성하기"""
#     print(request)
#
#     return JSONResponse(status_code=200, content={})

from fastapi import UploadFile

# @fileupload_router.post(
#     path="",
#     summary="test"
# )
# def file_upload_example(
#         upload_files: UploadFile = Form(default=None)
# ):
#     return JSONResponse(status_code=200, content={})

from starlette.datastructures import FormData


@fileupload_router.post(
    path="",
    summary="testv2",

)
def file_upload_example(
        upload_files: List[UploadFile] = FormData()
):
    print(upload_files)

    return JSONResponse(status_code=200, content={})
