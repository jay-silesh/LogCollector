from typing import List
import json

from src.constants.response_constants import LOGS, OFFSET
from src.entities.log import Log
from src.entities.response import Response


class AggregateResponse(object):
    def __init__(self):
        self._responses = {}

    def add_response(self, server, response):
        self._responses[server] = response

    def get_response(self):
        return json.dumps(self._responses, indent=2)
