
class Server(object):
    def __init__(self, ip_with_port):
        ip_with_port = ip_with_port.split(":")
        self._ip = ip_with_port[0]
        self._port = ip_with_port[1]

    def __str__(self):
        return "IP:%s Port:%s" % (self.ip, self.port)

    def __repr__(self):
        return "IP:%s Port:%s" % (self.ip, self.port)

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port
