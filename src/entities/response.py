import json
from http.client import responses
from typing import List

from constants.response_constants import LOGS, OFFSET, STATUS_MSG, STATUS_CODE
from entities.log import Log


class Response(object):
    def __init__(self):
        self._logs: List[Log] = []
        self._offset = None
        self._status_code = None

    def add_logs(self, logs):
        self._logs: List[Log] = logs

    def add_status_code(self, code: int):
        self._status_code = code

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
        tmp_dict = {LOGS: self._logs}
        if self._offset is not None:
            tmp_dict[OFFSET] = self._offset
        if self._status_code is not None:
            tmp_dict[STATUS_MSG] = responses[self._status_code].rstrip().lstrip()
            tmp_dict[STATUS_CODE] = self._status_code
        return tmp_dict

    def get_response(self):
        return json.dumps(self.build_dict(), indent=2)
