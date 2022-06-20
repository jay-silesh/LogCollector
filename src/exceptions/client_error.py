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

    # 400 Bad request
    # 404 file not found
    # 408 Request timed out
    @property
    def code(self):
        if self._code == ClientErrorCode.FILE_NOT_FOUND:
            return 404

        # Send ClientErrorCode.BAD_REQUEST by default
        return 400
