from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from src.entities.request import Request
from src.exceptions.client_error import ClientError
from src.exceptions.server_error import ServerError

"""
            # 200 OK
            # 204 is no content
            # 206 is partition content
"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query: str = urlparse(self.path).query
            http_request: Request = Request(query)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()

            self.send_error(501, "Server Implementation not ready!")
            # self.wfile.write(bytes(message, "utf8"))
        except ClientError as e:
            self.send_error(e.code, e.err_msg)
        except NotImplementedError as e:
            self.send_error(500, "Implementation missing!")
        except ServerError as e:
            self.send_response(500, e.err_msg)
        except Exception as e:
            self.send_response(500, "Unknown Error!")


with HTTPServer(('', 8000), handler) as server:
    print("Starting server on 8000")
    server.serve_forever()
