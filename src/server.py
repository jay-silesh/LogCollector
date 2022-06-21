from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from typing import List
import logging
from src.collector import serve_request
from src.entities.log import Log
from src.entities.request import Request
from src.entities.response import Response
from src.exceptions.client_error import ClientError
from src.exceptions.server_error import ServerError

"""
            # 200 OK
            # 204 is no content
            # 206 is partition content
"""


def _handle_request(query) -> Response:
    http_request: Request = Request(query)
    return serve_request(http_request)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            response: Response = _handle_request(urlparse(self.path).query)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(response.get_response(), 'utf-8'))
        except ClientError as e:
            self.send_error(e.code, e.err_msg)
        except NotImplementedError as e:
            logging.exception('NotImplementedError Failure', exc_info=True)
            self.send_error(500, "Implementation missing!")
        except ServerError as e:
            logging.exception('Server error', e)
            self.send_response(500, e.err_msg)
        except Exception as e:
            print(8)
            logging.exception(e, exc_info=True)
            self.send_response(500, "Unknown Error!")


with HTTPServer(('', 8000), handler) as server:
    print("Starting server on 8000")
    server.serve_forever()
