class Configuration(object):
    """Management Configuration"""

    def __init__(self, http_client, virtual_host):
        self.http_client = http_client
        self.virtual_host = virtual_host


class ManagementHandler(object):
    """Management Api Operations Handler (e.g. Queue, Exchange)"""

    def __init__(self, config):
        self.config = config
