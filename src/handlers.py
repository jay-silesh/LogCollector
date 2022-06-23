import threading

from constants.common_constants import MAX_LOGS_COUNT_LIMIT
from entities.aggregate_response import AggregateResponse
from entities.request import Request
from entities.response import Response
from exceptions.client_error import ClientError, ClientErrorCode
from implementations.log_file_reader_base_impl import LogFileReaderBaseImpl
from utils.http_utils import get_http_response_code, send_get_request
from utils.sugared_logger import SugaredLogger

logger = SugaredLogger()


def __serve_request(request: Request) -> Response:
    log_file_reader = LogFileReaderBaseImpl(request.file_name)
    response = Response()
    logger.logger.warning(request)
    if not log_file_reader.is_file_exists():
        raise ClientError("File does not exists", ClientErrorCode.FILE_NOT_FOUND)
    logger.logger.info("Successfully read file %s", request.file_name)

    # TODO add condition for privileges!
    logs, logs_offset = log_file_reader.read_logs(request.count, request.offset, request.keywords)
    response.add_logs(logs[:MAX_LOGS_COUNT_LIMIT])
    if len(logs) > MAX_LOGS_COUNT_LIMIT:
        response.add_offset(request.offset + response.get_logs_count())
    return response


def __fire_child_node_request(aggr_response, child_server, child_url):
    final_url = "http://%s/logs/%s" % (child_server, child_url)
    try:
        status_code, response_dict = send_get_request(final_url)
        if 200 <= status_code < 300:
            aggr_response.add_response_dict(child_server, status_code, response_dict)
        else:
            aggr_response.add_response_dict(child_server, status_code, response_dict)
    except Exception as e:
        aggr_response.add_response_dict(child_server, get_http_response_code(e), response_dict=None)


def handle_request(url) -> Response:
    http_request = Request(url, is_master_node=False)
    return __serve_request(http_request)


def handle_master_node_request(url) -> AggregateResponse:
    http_request = Request(url, is_master_node=True)
    child_url = http_request.child_url
    aggr_response = AggregateResponse()
    threads = []
    for child_server in http_request.servers:
        t = threading.Thread(target=__fire_child_node_request, args=(aggr_response, child_server, child_url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return aggr_response
