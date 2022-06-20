from src.constants.request_constants import FILE, COUNT, KEYWORDS
from src.exceptions.client_error import ClientError


class Request(object):
    __required_params = [FILE]
    __optional_params = [COUNT, KEYWORDS]
    __DEFAULT_COUNT_LIMIT = 100

    def __init__(self, http_request_query):
        self._query_components = dict(qc.split("=") for qc in http_request_query.split("&"))
        self.__validate()
        self._file_name = self._query_components.get(FILE)
        self._count = self._query_components.get(COUNT, Request.__DEFAULT_COUNT_LIMIT)
        self._keywords = self._query_components.get(KEYWORDS, [])

    def __validate(self):
        components = self._query_components
        for p in Request.__required_params:
            if p not in components:
                raise ClientError("File name missing from the request")

    def get_file_name(self):
        return self._file_name

