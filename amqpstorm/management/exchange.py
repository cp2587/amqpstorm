import json

from amqpstorm.compatibility import urlparse
from amqpstorm.management.base import ManagementHandler

API_EXCHANGE = 'exchanges/%s/%s'
API_EXCHANGES = 'exchanges'
API_EXCHANGES_VIRTUAL_HOST = 'exchanges/%s'
API_EXCHANGE_BINDINGS = 'exchanges/%s/%s/bindings/source'
API_EXCHANGE_BIND = 'bindings/%s/e/%s/e/%s'
API_EXCHANGE_UNBIND = 'bindings/%s/e/%s/e/%s/%s'


class Exchange(ManagementHandler):
    def get(self, exchange):
        """Get Exchange details.

        :param str exchange: Exchange name

        :rtype: dict
        """
        return self.config.http_client.get(
            API_EXCHANGE
            % (
                self.config.virtual_host,
                exchange)
        )

    def list(self, show_all=False):
        """List Exchanges.

        :param bool show_all: List all Exchanges.

        :rtype: list
        """
        if show_all:
            return self.config.http_client.get(API_EXCHANGES)
        return self.config.http_client.get(
            API_EXCHANGES_VIRTUAL_HOST % self.config.virtual_host
        )

    def declare(self, exchange='', exchange_type='direct', passive=False,
                durable=False, auto_delete=False, arguments=None):
        """Declare an Exchange.

        :param str exchange: Exchange name
        :param str exchange_type: Exchange type
        :param bool passive: Do not create
        :param bool durable: Durable exchange
        :param bool auto_delete: Automatically delete when not in use
        :param dict arguments: Exchange key/value arguments

        :rtype: None
        """
        if passive:
            return self.get(exchange)
        exchange_payload = json.dumps(
            {
                'durable': durable,
                'auto_delete': auto_delete,
                'internal': False,
                'type': exchange_type,
                'arguments': arguments or {},
                'vhost': urlparse.unquote(self.config.virtual_host)
            }
        )
        return self.config.http_client.put(API_EXCHANGE %
                                           (
                                               self.config.virtual_host,
                                               exchange
                                           ),
                                           payload=exchange_payload)

    def delete(self, exchange):
        """Delete an Exchange.

        :param str exchange: Exchange name

        :rtype: dict
        """
        return self.config.http_client.delete(API_EXCHANGE %
                                              (
                                                  self.config.virtual_host,
                                                  exchange
                                              ))

    def bindings(self, exchange):
        """Get Exchange bindings.

        :param str exchange: Exchange name

        :rtype: list
        """
        return self.config.http_client.get(API_EXCHANGE_BINDINGS %
                                           (
                                               self.config.virtual_host,
                                               exchange
                                           ))

    def bind(self, source, destination, routing_key, arguments=None):
        """Bind an Exchange.

        :param str source: Source Exchange name
        :param str destination: Destination Exchange name
        :param str routing_key: The routing key to use
        :param dict arguments: Bind key/value arguments

        :rtype: None
        """
        bind_payload = json.dumps({
            'destination': destination,
            'destination_type': 'e',
            'routing_key': routing_key,
            'source': source,
            'arguments': arguments or {},
            'vhost': self.config.virtual_host
        })
        return self.config.http_client.post(API_EXCHANGE_BIND %
                                            (
                                                self.config.virtual_host,
                                                source,
                                                destination
                                            ),
                                            payload=bind_payload)

    def unbind(self, source, destination, routing_key, properties_key=None):
        """Unbind an Exchange.

        :param str source: Source Exchange name
        :param str destination: Destination Exchange name
        :param str routing_key: The routing key to use
        :param str properties_key:

        :rtype: None
        """
        unbind_payload = json.dumps({
            'destination': destination,
            'destination_type': 'e',
            'properties_key': properties_key or routing_key,
            'source': source,
            'vhost': self.config.virtual_host
        })
        return self.config.http_client.delete(API_EXCHANGE_UNBIND %
                                              (
                                                  self.config.virtual_host,
                                                  source,
                                                  destination,
                                                  properties_key or routing_key
                                              ),
                                              payload=unbind_payload)
