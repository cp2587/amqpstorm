from amqpstorm.compatibility import quote
from amqpstorm.management.base import Configuration
from amqpstorm.management.basic import Basic
from amqpstorm.management.channel import Channel
from amqpstorm.management.connection import Connection
from amqpstorm.management.exchange import Exchange
from amqpstorm.management.http_client import HTTPClient
from amqpstorm.management.queue import Queue
from amqpstorm.management.user import User
from amqpstorm.management.virtual_host import VirtualHost

API_ALIVENESS_TEST = 'aliveness-test/%s'
API_NODES = 'nodes'
API_OVERVIEW = 'overview'
API_WHOAMI = 'whoami'
API_TOP = 'top/%s'


class ManagementApi(object):
    def __init__(self, api_url, username, password, virtual_host='/',
                 timeout=3):
        http_client = HTTPClient(api_url, username, password, timeout=timeout)
        self.config = Configuration(http_client, quote(virtual_host, ''))
        self.basic = Basic(self.config)
        self.channel = Channel(self.config)
        self.connection = Connection(self.config)
        self.exchange = Exchange(self.config)
        self.queue = Queue(self.config)
        self.user = User(self.config)
        self.virtual_host = VirtualHost(self.config)

    def aliveness_test(self):
        """Aliveness Test.

        :rtype: dict
        """
        return self.config.http_client.get(API_ALIVENESS_TEST %
                                           self.config.virtual_host)

    def overview(self):
        """Get Overview.

        :rtype: dict
        """
        return self.config.http_client.get(API_OVERVIEW)

    def nodes(self):
        """Get Nodes.

        :rtype: dict
        """
        return self.config.http_client.get(API_NODES)

    def top(self):
        """Top Processes.

        :rtype: list
        """
        nodes = []
        for node in self.nodes():
            nodes.append(self.config.http_client.get(API_TOP % node['name']))
        return nodes

    def whoami(self):
        """Who am I?

        :rtype: dict
        """
        return self.config.http_client.get(API_WHOAMI)
