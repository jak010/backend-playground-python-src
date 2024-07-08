import copy
import shutil
from typing import List
import threading

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

fileupload_router = APIRouter(tags=['FILE_UPLOAD_OBJECT'], prefix='/api/v1')


class FileUploadTask(threading.Thread):

    def __init__(self, upload_files: List[UploadFile]):
        # self.upload_files = copy.deepcopy(upload_files)  # Solved.. ?
        self.upload_files = upload_files  # Solved.. ?
        super().__init__()

    def run(self) -> None:
        import time
        time.sleep(2)
        print("File Upload Start")
        for file_upload in self.upload_files:
            with open(file_upload.filename, "wb") as file:
                shutil.copyfileobj(file_upload.file, file)
                file.close()
        print("File Upload End")


@fileupload_router.post(path="")
def file_uploads(
        upload_files: List[UploadFile]
):
    """ post 생성하기"""

    task = FileUploadTask(upload_files)
    task.start()

    return JSONResponse(status_code=200, content={})
