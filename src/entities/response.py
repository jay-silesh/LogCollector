import json
from http.client import responses
from typing import List

from src.constants.response_constants import LOGS, OFFSET, STATUS
from src.entities.log import Log


class Response(object):
    def __init__(self):
        self._logs: List[Log] = []
        self._offset = None
        self._status = None

    def add_logs(self, logs):
        self._logs: List[Log] = logs

    def add_status_code(self, code: int):
        self._status = responses[code].rstrip().lstrip()

    def add_offset(self, offset):
        self._offset = offset

    @property
    def logs(self) -> List[Log]:
        return self._logs

    @property
    def is_offset(self) -> bool:
        return True if self._offset else False

    @staticmethod
    def build_with_error_code(code):
        r = Response()
        r.add_status_code(code)
        return r

    def build_dict(self):
        tmp_dict = {}
        if self._logs:
            tmp_dict[LOGS] = self._logs
        if self._offset is not None:
            tmp_dict[OFFSET] = self._offset
        if self._status is not None:
            tmp_dict[STATUS] = self._status
        return tmp_dict

    def get_response(self):
        return json.dumps(self.build_dict(), indent=2)
