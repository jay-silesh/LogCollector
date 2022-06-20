class ClientError(Exception):
    """Raised when a bad/invalid input is called by the client"""
    def __init__(self, err_msg):
        self.err_msg = err_msg


