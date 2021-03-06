import getopt
import logging
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from constants.common_constants import URL_LOGS_AGGREGATE, URL_LOGS
from entities.aggregate_response import AggregateResponse
from entities.response import Response
from exceptions.client_error import ClientError, ClientErrorCode
from exceptions.server_error import ServerError
from handlers import handle_request, handle_master_node_request
from utils.http_utils import get_http_response_code

DEFAULT_PORT = 8000


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url_path = urlparse(self.path).path
            final_resp = ""
            if url_path == URL_LOGS_AGGREGATE:  # TODO make this an interface!
                response: AggregateResponse = handle_master_node_request(self.path)
                final_resp = response.get_response()
            elif url_path == URL_LOGS:
                response: Response = handle_request(self.path)
                final_resp = response.get_response()
            else:
                raise ClientError("Bad URL path", ClientErrorCode.BAD_REQUEST)

            print("Got the response as ", response)
            self.send_response(get_http_response_code(response))
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(final_resp, 'utf-8'))

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


def main(argv):
    port = DEFAULT_PORT
    try:
        opts, args = getopt.getopt(argv, "hp:", ["port="])
    except getopt.GetoptError:
        print('server.py -p <port>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('server.py -p <port>')
            sys.exit()
        elif opt in ("-p", "--port"):
            port = int(arg)
    with HTTPServer(('', port), handler) as server:
        print("Starting server on ", port)
        server.serve_forever()


if __name__ == "__main__":
    main(sys.argv[1:])
