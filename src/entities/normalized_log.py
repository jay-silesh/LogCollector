
# Equivalent of typeDef
from datetime import datetime

from src.entities.log import Log


class NormalizedLog(object):
    def __init__(self, input_log: Log):
        self._log: Log = input_log
        self._ts: datetime = self.parse_date()

    def parse_date(self):
        raise NotImplementedError("Parse date not implemented")

    def get_log(self) -> Log:
        return self._log

    def get_ts(self) -> datetime:
        return self._ts
