from typing import List

from src.constants.common_constants import DEFAULT_LOG_COUNT_LIMIT
from src.constants.request_constants import FILE, COUNT, KEYWORDS, OFFSET, SERVERS
from src.entities.server import Server
from src.exceptions.client_error import ClientError, ClientErrorCode


class Request(object):
    __required_params = [FILE]
    __required_params_master_node = [FILE, SERVERS]
    __optional_params = [COUNT, KEYWORDS]

    def __init__(self, http_request_query, is_master_node=False):
        self._query_components = dict(qc.split("=") for qc in http_request_query.split("&"))
        self.__validate(is_master_node)
        self._file_name = self._query_components.get(FILE)
        self._servers: List[Server] = [Server(addr) for addr in set(self._query_components.get(SERVERS, "").split(","))]
        self._count = int(self._query_components.get(COUNT, DEFAULT_LOG_COUNT_LIMIT))
        self._keywords = set(self._query_components.get(KEYWORDS, "").split(","))
        self._offset = int(self._query_components.get(OFFSET, 0))  # Default offset == 0 (Starting EOF)

    def __validate(self, is_master_node):
        components = self._query_components
        required_params = Request.__required_params if not is_master_node else Request.__required_params_master_node

        for p in required_params:
            if p not in components or not self._query_components.get(p):
                raise ClientError("%s param missing from the request" % p, ClientErrorCode.BAD_REQUEST)

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
    def keywords(self) -> set:
        return self._keywords

    @property
    def offset(self):
        return self._offset

    @property
    def servers(self) -> List[Server]:
        return self._servers
