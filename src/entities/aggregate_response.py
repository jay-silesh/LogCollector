import json
from http.client import responses

from src.constants.response_constants import STATUS
from src.entities.response import Response


class AggregateResponse(object):
    def __init__(self):
        self._responses = {}

    def add_response_dict(self, server, status_code: int, response_dict: dict = None):
        if not response_dict:
            response: Response = Response.build_with_error_code(status_code)
            response_dict = response.build_dict()
        else:
            response_dict[STATUS] = responses[status_code].rstrip().lstrip()
        self._responses[server] = response_dict

    def add_error_response(self, server, status_code: int):
        response: Response = Response.build_with_error_code(status_code)
        self._responses[server] = response.build_dict()

    def get_response(self):
        tmp_dict = {}
        for server, response in self._responses.items():
            if isinstance(response, Response):
                tmp_dict[server] = response.get_response()
                continue
            tmp_dict[server] = response
        return json.dumps(tmp_dict, indent=2)
