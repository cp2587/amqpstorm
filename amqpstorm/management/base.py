from amqpstorm.compatibility import quote


class Configuration(object):
    """Management Configuration"""

    def __init__(self, http_client, virtual_host):
        self.http_client = http_client
        self.virtual_host = quote(virtual_host, '')

    def set_virtual_host(self, virtual_host):
        """Change the Virtual Host used by the Management Api.

        :param virtual_host: Virtual Host name

        :return:
        """
        self.virtual_host = quote(virtual_host, '')


class ManagementHandler(object):
    """Management Api Operations Handler (e.g. Queue, Exchange)"""

    def __init__(self, config):
        self.config = config
