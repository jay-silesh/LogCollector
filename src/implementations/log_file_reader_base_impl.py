import collections
import os
import tempfile
from abc import ABC
from pathlib import Path
from typing import List

from entities.log import Log
from entities.offset import Offset
from exceptions.client_error import ClientError, ClientErrorCode
from interfaces.log_file_reader_base import LogFileReaderBase


class LogFileReaderBaseImpl(LogFileReaderBase, ABC):
    __UNIX_LOG_FILES_DIR_PATH_PREFIX = "/var/log/"

    def __init__(self, file_name: str):
        super().__init__(file_name)

    def read_logs(self, n: int, offset: Offset = 0, keywords: set = None) -> (List[Log], Offset):
        def yield_lines(fname):
            with open(fname) as qfile:
                qfile.seek(0, os.SEEK_END)
                position = qfile.tell()
                line = ''
                while position >= 0:
                    qfile.seek(position)
                    next_char = qfile.read(1)
                    if next_char == "\n":
                        yield line[::-1]
                        line = ''
                    else:
                        line += next_char
                    position -= 1
                yield line[::-1]

        queue = collections.deque([], n)
        next_offset = 0
        for count, l in enumerate(yield_lines(self.file_path)):
            if count < offset:
                continue
            queue.append(l)
            if len(queue) >= n:
                next_offset = count + 1
                break
        return list(queue), next_offset

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
