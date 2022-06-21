from src.constants.common_constants import DEFAULT_LOG_COUNT_LIMIT
from src.constants.request_constants import FILE, COUNT, KEYWORDS
from src.exceptions.client_error import ClientError, ClientErrorCode


class Request(object):
    __required_params = [FILE]
    __optional_params = [COUNT, KEYWORDS]

    def __init__(self, http_request_query):
        self._query_components = dict(qc.split("=") for qc in http_request_query.split("&"))
        self.__validate()
        self._file_name = self._query_components.get(FILE)
        self._count = int(self._query_components.get(COUNT, DEFAULT_LOG_COUNT_LIMIT))
        self._keywords = self._query_components.get(KEYWORDS, "").split(",")

    def __validate(self):
        components = self._query_components
        for p in Request.__required_params:
            if p not in components:
                raise ClientError("File name missing from the request", ClientErrorCode.FILE_NOT_FOUND)

    def __str__(self):
        return "FileName:%s Count:%s Keywords:%s" % (self.file_name, self.count, self.keywords)

    def __repr__(self):
        return "FileName:%s Count:%s Keywords:%s" % (self.file_name, self.count, self.keywords)

    @property
    def file_name(self):
        return self._file_name

    @property
    def count(self):
        return self._count

    @property
    def keywords(self):
        return self._keywords
