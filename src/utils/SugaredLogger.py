import logging

logging.basicConfig(level=logging.DEBUG)


class SugaredLogger(object):
    def __init__(self, name=None):
        self._logger: logging.Logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

    @property
    def logger(self):
        return self._logger
