import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from src.collector import serve_request
from src.constants.common_constants import URL_LOGS_AGGREGATE, URL_LOGS
from src.entities.aggregate_response import AggregateResponse
from src.entities.request import Request
from src.entities.response import Response
from src.exceptions.client_error import ClientError, ClientErrorCode
from src.exceptions.server_error import ServerError
from src.utils.http_utils import get_http_response_code, send_get_request

PORT = 8000


def _handle_request(url) -> Response:
    http_request = Request(url, is_master_node=False)
    return serve_request(http_request)


def fire_child_node_request(aggr_response, child_server, child_url):

    final_url = "http://%s/logs/%s" % (child_server, child_url)
    try:
        status_code, response_dict = send_get_request(final_url)
        if 200 <= status_code < 300:
            aggr_response.add_response_dict(child_server, status_code, response_dict)
        else:
            aggr_response.add_response_dict(child_server, status_code, response_dict)
    except Exception as e:
        aggr_response.add_response_dict(child_server, get_http_response_code(e), response_dict=None)


def _handle_master_node_request(url) -> AggregateResponse:
    http_request = Request(url, is_master_node=True)
    child_url = http_request.child_url
    aggr_response = AggregateResponse()
    threads = []
    for child_server in http_request.servers:
        t = threading.Thread(target=fire_child_node_request, args=(aggr_response, child_server, child_url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return aggr_response


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url_path = urlparse(self.path).path
            if url_path == URL_LOGS_AGGREGATE:
                response: AggregateResponse = _handle_master_node_request(self.path)
            elif url_path == URL_LOGS:
                response: Response = _handle_request(self.path)
            else:
                raise ClientError("Bad URL path", ClientErrorCode.BAD_REQUEST)

            self.send_response(get_http_response_code(response))
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(response.get_response(), 'utf-8'))

        except ClientError as e:
            self.send_error(get_http_response_code(e), e.err_msg)
        except ConnectionError as e:
            self.send_response(get_http_response_code(e), "Bad Connection")
        except NotImplementedError as e:
            logging.exception('NotImplementedError Failure', exc_info=True)
            self.send_error(get_http_response_code(e), "Implementation missing!")
        except ServerError as e:
            logging.exception('Server error', e)
            self.send_response(get_http_response_code(e), e.err_msg)
        except Exception as e:
            logging.exception(e, exc_info=True)
            self.send_response(get_http_response_code(e), "Unknown Error!")


with HTTPServer(('', PORT), handler) as server:
    print("Starting server on ", PORT)
    server.serve_forever()
