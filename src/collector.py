from typing import List

from src.constants.common_constants import MAX_LOGS_COUNT_LIMIT
from src.entities.log import Log
from src.entities.request import Request
from src.entities.response import Response
from src.exceptions.client_error import ClientError, ClientErrorCode
from src.implementations.log_file_reader_base_impl import LogFileReaderBaseImpl
from src.utils.SugaredLogger import SugaredLogger

logger = SugaredLogger()


def serve_request(request: Request) -> Response:
    log_file_reader = LogFileReaderBaseImpl(request.file_name)
    response = Response()
    logger.logger.warning(request)
    if not log_file_reader.is_file_exists():
        raise ClientError("File does not exists", ClientErrorCode.FILE_NOT_FOUND)
    logger.logger.info("Successfully read file %s", request.file_name)

    # TODO add condition for privileges!
    logs = log_file_reader.read_logs(request.count, request.offset)
    print(len(logs))
    if len(logs) > MAX_LOGS_COUNT_LIMIT:
        total_logs = log_file_reader.get_total_size()
        offset = total_logs - request.count + MAX_LOGS_COUNT_LIMIT
        response.add_offset(offset)
    response.add_logs(logs[:MAX_LOGS_COUNT_LIMIT])
    return response
