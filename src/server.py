import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from src.collector import serve_request
from src.entities.request import Request
from src.entities.response import Response
from src.exceptions.client_error import ClientError, ClientErrorCode
from src.exceptions.server_error import ServerError
from src.utils.http_utils import get_http_response_code

PORT = 8000


def _handle_request(url) -> Response:
    http_request = Request(url, is_master_node=False)
    return serve_request(http_request)


def _handle_master_node_request(url) -> Response:
    http_request = Request(url, is_master_node=True)
    print(http_request.servers)
    raise NotImplementedError


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url_path = urlparse(self.path).path
            if url_path == "/logs/aggregate/":
                response: Response = _handle_master_node_request(self.path)
            elif url_path == "/logs/":
                response: Response = _handle_request(self.path)
            else:
                raise ClientError("Bad URL path", ClientErrorCode.BAD_REQUEST)

            self.send_response(get_http_response_code(response))
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(response.get_response(), 'utf-8'))

        except ClientError as e:
            self.send_error(get_http_response_code(e), e.err_msg)
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
