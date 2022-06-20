from abc import ABC
from typing import List

from src.entities.log import Log
from src.entities.log_file import LogFile
from src.interfaces.log_file_reader_base import LogFileReaderBase


class LogFileReaderBaseImpl(LogFileReaderBase, ABC):
    def __init__(self):
        super().__init__()

    def _read_logs(self, log_file: LogFile) -> List[Log]:
        raise NotImplementedError

    def _open_log_file(self, file_path: str) -> LogFile:
        raise NotImplementedError
