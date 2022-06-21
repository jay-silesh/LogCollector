from abc import abstractmethod
# TODO: Add documentation of what each of the interface should be implementing!
from typing import List

from src.entities.log import Log


class LogFileReaderBase(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._abs_path = self.get_abs_path()

    @property
    def file_name(self):
        return self._file_name

    @property
    def file_path(self):
        return self._abs_path

    ########################################################################
    #                                                                      #
    #                Abstract Methods                                      #
    #                                                                      #
    ########################################################################
    @abstractmethod
    def get_abs_path(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def read_logs(self, n: int, offset: int = 0, keywords: set = None) -> List[Log]:
        raise NotImplementedError

    @abstractmethod
    def is_file_exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_total_size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def has_privileges(self) -> bool:
        raise NotImplementedError
