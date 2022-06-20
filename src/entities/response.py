from typing import List

from src.entities.log import Log


class Response(object):
    def __init__(self, logs):
        self._logs: List[Log] = logs

    def get_response(self):
        raise NotImplementedError
