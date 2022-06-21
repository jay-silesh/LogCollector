from typing import List
import json

from src.constants.response_constants import LOGS, OFFSET
from src.entities.log import Log


class Response(object):
    def __init__(self):
        self._logs: List[Log] = []
        self._offset = None

    def add_logs(self, logs):
        self._logs: List[Log] = logs

    def add_offset(self, offset):
        self._offset = offset

    @property
    def logs(self) -> List[Log]:
        return self._logs

    @property
    def is_offset(self) -> bool:
        return True if self._offset else False

    def get_response(self):
        tmp_dict = {LOGS: self._logs}
        if self._offset is not None:
            tmp_dict[OFFSET] = self._offset
        return json.dumps(tmp_dict, indent=2)
