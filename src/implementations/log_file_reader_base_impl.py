from abc import ABC
from typing import List
from pathlib import Path

from src.entities.log import Log
from src.entities.log_file import LogFile
from src.exceptions.client_error import ClientError, ClientErrorCode
from src.interfaces.log_file_reader_base import LogFileReaderBase


class LogFileReaderBaseImpl(LogFileReaderBase, ABC):
    __UNIX_LOG_FILES_DIR_PATH_PREFIX = "/var/log/"

    def __init__(self, file_name: str):
        super().__init__(file_name)

    def read_logs(self, n: int) -> List[Log]:
        with open(self.file_path) as file:
            # loop to read iterate
            # last n lines and print it
            return [line for line in (file.readlines()[-n:])]

    def is_file_exists(self) -> bool:
        path = Path(self.file_path)
        if path.is_file():
            return True
        return False

    def has_privileges(self) -> bool:
        raise NotImplementedError

    def get_abs_path(self):
        file_name = self.file_name
        if not file_name:
            raise ClientError("Empty FileName", ClientErrorCode.BAD_REQUEST)
        while file_name[0] == "/":
            file_name = file_name[1:]
        return LogFileReaderBaseImpl.__UNIX_LOG_FILES_DIR_PATH_PREFIX + file_name
