from typing import List

from src.entities.log import Log
from src.entities.request import Request
from src.implementations.log_file_reader_base_impl import LogFileReaderBaseImpl
from src.utils.SugaredLogger import SugaredLogger

logger = SugaredLogger()


def get_logs(request: Request) -> List[Log]:
    logFileReader = LogFileReaderBaseImpl(request.file_name)
    logs = logFileReader.read_logs(request.count)
    logger.logger.warning("Request Info", request)
    logger.logger.info("Successfully read file %s with %d logs", request.file_name, len(logs))
    raise NotImplementedError()
