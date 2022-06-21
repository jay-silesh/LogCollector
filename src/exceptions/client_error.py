import enum


class ClientErrorCode(enum.Enum):
    UNKNOWN = 0
    BAD_REQUEST = 1
    FILE_NOT_FOUND = 2


class ClientError(Exception):
    """Raised when a bad/invalid input is called by the client"""

    def __init__(self, err_msg: str, code: ClientErrorCode):
        self.err_msg = err_msg
        self._code = code

    @property
    def code(self):
        return self._code
