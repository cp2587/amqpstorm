import json

from amqpstorm.compatibility import urlparse
from amqpstorm.management.base import ManagementHandler

API_QUEUE = 'queues/%s/%s'
API_QUEUE_PURGE = 'queues/%s/%s/contents'
API_QUEUES = 'queues'
API_QUEUES_VIRTUAL_HOST = 'queues/%s'
API_QUEUE_BINDINGS = 'queues/%s/%s/bindings'
API_QUEUE_BIND = 'bindings/%s/e/%s/q/%s'
API_QUEUE_UNBIND = 'bindings/%s/e/%s/q/%s/%s'


class Queue(ManagementHandler):
    def get(self, queue):
        """Get Queue details.

        :param queue: Queue name

        :rtype: dict
        """
        return self.config.http_client.get(
            API_QUEUE % (
                self.config.virtual_host,
                queue
            )
        )

    def list(self, show_all=False):
        """List Queues.

        :param bool show_all: List all Queues.

        :rtype: list
        """
        if show_all:
            return self.config.http_client.get(API_QUEUES)
        return self.config.http_client.get(
            API_QUEUES_VIRTUAL_HOST % self.config.virtual_host
        )

    def declare(self, queue='', passive=False, durable=False,
                auto_delete=False, arguments=None):
        """Declare a Queue.

        :param str queue: Queue name
        :param bool passive: Do not create
        :param bool durable: Durable queue
        :param bool auto_delete: Automatically delete when not in use
        :param dict arguments: Queue key/value arguments

        :rtype: dict
        """
        if passive:
            return self.get(queue)
        queue_payload = json.dumps(
            {
                'durable': durable,
                'auto_delete': auto_delete,
                'arguments': arguments or {},
                'vhost': urlparse.unquote(self.config.virtual_host)
            }
        )
        return self.config.http_client.put(
            API_QUEUE % (self.config.virtual_host, queue),
            payload=queue_payload)

    def delete(self, queue):
        """Delete a Queue.

        :param str queue: Queue name

        :rtype: dict
        """
        return self.config.http_client.delete(API_QUEUE %
                                              (
                                                  self.config.virtual_host,
                                                  queue
                                              ))

    def purge(self, queue):
        """Purge a Queue.

        :param str queue: Queue name

        :rtype: None
        """
        return self.config.http_client.delete(API_QUEUE_PURGE %
                                              (
                                                  self.config.virtual_host,
                                                  queue
                                              ))

    def bindings(self, queue):
        """Get Queue bindings.

        :param str queue: Queue name

        :rtype: list
        """
        return self.config.http_client.get(API_QUEUE_BINDINGS %
                                           (
                                               self.config.virtual_host,
                                               queue
                                           ))

    def bind(self, queue, exchange, routing_key, arguments=None):
        """Bind a Queue.

        :param str queue: Queue name
        :param str exchange: Exchange name
        :param str routing_key: The routing key to use
        :param dict arguments: Bind key/value arguments

        :rtype: None
        """
        bind_payload = json.dumps({
            'destination': queue,
            'destination_type': 'q',
            'routing_key': routing_key,
            'source': exchange,
            'arguments': arguments or {},
            'vhost': self.config.virtual_host
        })
        return self.config.http_client.post(API_QUEUE_BIND %
                                            (
                                                self.config.virtual_host,
                                                exchange,
                                                queue
                                            ),
                                            payload=bind_payload)

    def unbind(self, queue, exchange, routing_key, properties_key=None):
        """Unbind a Queue.

        :param str queue: Queue name
        :param str exchange: Exchange name
        :param str routing_key: The routing key to use
        :param str properties_key:

        :rtype: None
        """
        unbind_payload = json.dumps({
            'destination': queue,
            'destination_type': 'q',
            'properties_key': properties_key or routing_key,
            'source': exchange,
            'vhost': self.config.virtual_host
        })
        return self.config.http_client.delete(API_QUEUE_UNBIND %
                                              (
                                                  self.config.virtual_host,
                                                  exchange,
                                                  queue,
                                                  properties_key or routing_key
                                              ),
                                              payload=unbind_payload)
