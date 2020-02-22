import os
import uuid
import shutil
from typing import List
from pathlib import Path
from . import storage

__main_service = None


def init_main_service(path):
    global __main_service
    __main_service = Uploads(path)


class Uploads:

    def __init__(self, path: str):
        self.__path = path

    def upload(self, page_id, file_name, stream):
        file_id = str(uuid.uuid4())
        page_path = os.path.join(self.__path, str(page_id))
        file_path = os.path.join(page_path, file_id)
        Path(page_path).mkdir(parents=True, exist_ok=True)

        with open(file_path, 'wb') as fp:
            shutil.copyfileobj(stream, fp)

        storage_service = storage.main_service()
        storage_service.register_attachement(page_id, file_name, file_id)

    def read(self, page_id, file_name) -> str:
        storage_service = storage.main_service()
        file_id = storage_service.get_attachement_file_id(page_id, file_name)
        file_path = os.path.join(self.__path, str(page_id), file_id)
        return file_path

    def list(self, page_id) -> List[str]:
        storage_service = storage.main_service()
        uploads = storage_service.get_page_attachments(page_id)
        file_names = [u.file_name for u in uploads]
        return file_names


def main_service() -> Uploads:
    if __main_service:
        return __main_service
    else:
        raise Exception('uploads main service is not initialized')
