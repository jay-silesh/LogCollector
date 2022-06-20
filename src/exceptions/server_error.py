import enum


class ServerErrorCode(enum.Enum):
    UNKNOWN = 0
    INTERNAL_ERROR = 1
    NOT_IMPLEMENTED = 2


class ServerError(Exception):
    def __init__(self, err_msg, code: ServerErrorCode):
        self.err_msg = err_msg
        self._code = code

    @property
    def code(self):
        # 500 Server error
        # 501 Not implemented.
        # By default, throw ServerErrorCode.NOT_IMPLEMENTED
        return 501
