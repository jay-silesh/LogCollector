from typing import List
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from constants.common_constants import DEFAULT_LOG_COUNT_LIMIT, URL_LOGS_AGGREGATE, UNIX_LOG_FILES_DIR_PATH_PREFIX
from constants.request_constants import FILE, COUNT, KEYWORDS, OFFSET, SERVERS
from exceptions.client_error import ClientError, ClientErrorCode


class Request(object):
    __required_params = [FILE]
    __required_params_master_node = [FILE, SERVERS]
    __optional_params = [COUNT, KEYWORDS]

    def __init__(self, req_url, is_master_node=False):
        http_request_query = urlparse(req_url).query
        self._query_components = dict(qc.split("=") for qc in http_request_query.split("&"))
        self.__validate(is_master_node)
        self._file_name = self.__normalize_file_name(self._query_components.get(FILE))
        self._servers = []
        self._child_url = None
        self._count = int(self._query_components.get(COUNT, DEFAULT_LOG_COUNT_LIMIT))
        self._keywords = set(self._query_components.get(KEYWORDS, "").split(","))
        self._offset = int(self._query_components.get(OFFSET, 0))  # Default offset == 0 (Starting EOF)
        if is_master_node:
            self.__parse_child_nodes(req_url)

    def __normalize_file_name(self, file_name: str):
        if file_name.startswith(UNIX_LOG_FILES_DIR_PATH_PREFIX):
            return file_name.replace(UNIX_LOG_FILES_DIR_PATH_PREFIX, "")
        return file_name

    def __parse_child_nodes(self, url):
        u = urlparse(url)
        query = parse_qs(u.query, keep_blank_values=True)
        servers = query.pop(SERVERS, None)
        if len(servers) > 0:
            self._servers = servers[0].split(",")
        u = u._replace(query=urlencode(query, True))
        self._child_url = urlunparse(u)
        self._child_url = self._child_url.replace(URL_LOGS_AGGREGATE, "")

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
    def servers(self) -> List:
        return self._servers

    @property
    def child_url(self):
        return self._child_url
