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

    def read_logs(self, n: int, offset: int = 0) -> List[Log]:
        with open(self.file_path) as file:
            my_list = []
            lines = file.readlines()[::-1][offset:]
            # lines = lines[::-1]
            while n > 0 and lines:
                line = lines.pop(0).rstrip()
                if not line:
                    continue
                my_list.append(line)
                n -= 1
            return my_list

    def get_total_size(self) -> int:
        with open(self.file_path) as fp:
            return len(fp.readlines())

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
