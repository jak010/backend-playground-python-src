import threading
from fastapi import UploadFile
import shutil
from typing import List


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
