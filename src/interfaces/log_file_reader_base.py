import collections
import itertools
from abc import abstractmethod


# TODO: Add documentation of what each of the interface should be implementing!
from typing import List

from src.entities.log import Log
from src.entities.log_file import LogFile


class LogFileReaderBase(object):
    ########################################################################
    #                                                                      #
    #                Abstract Methods                                      #
    #                                                                      #
    ########################################################################
    @abstractmethod
    def _read_logs(self, log_file: LogFile) -> List[Log]:
        raise NotImplementedError

    @abstractmethod
    def _open_log_file(self, file_path: str) -> LogFile:
        raise NotImplementedError
