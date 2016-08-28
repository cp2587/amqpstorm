import json

from amqpstorm.compatibility import quote
from amqpstorm.compatibility import urlparse
from amqpstorm.management.base import ManagementHandler
from amqpstorm.message import Message

API_BASIC_PUBLISH = 'exchanges/%s/%s/publish'
API_BASIC_GET_MESSAGE = 'queues/%s/%s/get'


class Basic(ManagementHandler):
    def publish(self, body, routing_key, exchange='amq.default',
                properties=None, payload_encoding='string'):
        """Publish a Message.

        :param bytes|str|unicode body: Message payload
        :param str routing_key: Message routing key
        :param str exchange: The exchange to publish the message to
        :param dict properties: Message properties
        :param str payload_encoding: Payload encoding.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        exchange = quote(exchange, '')
        properties = properties or {}
        body = json.dumps(
            {
                'routing_key': routing_key,
                'payload': body,
                'payload_encoding': payload_encoding,
                'properties': properties,
                'vhost': urlparse.unquote(self.config.virtual_host)
            }
        )
        return self.config.http_client.post(API_BASIC_PUBLISH %
                                            (
                                                self.config.virtual_host,
                                                exchange),
                                            payload=body)

    def get(self, queue, requeue=False, to_dict=False, count=1, truncate=50000,
            encoding='auto'):
        """Get Messages.

        :param str queue: Queue name
        :param bool requeue: Re-queue message
        :param bool to_dict: Should incoming messages be converted to a
                    dictionary before delivery.
        :param int count: How many messages should we try to fetch.
        :param int truncate: The maximum length in bytes, beyond that the
                             server will truncate the message.
        :param str encoding: Message encoding.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: list
        """
        get_messages = json.dumps(
            {
                'count': count,
                'requeue': requeue,
                'encoding': encoding,
                'truncate': truncate,
                'vhost': urlparse.unquote(self.config.virtual_host)
            }
        )
        response = self.config.http_client.post(API_BASIC_GET_MESSAGE %
                                                (
                                                    self.config.virtual_host,
                                                    queue
                                                ),
                                                payload=get_messages)
        if to_dict:
            return response
        messages = []
        for message in response:
            if 'payload' in message:
                message['body'] = message.pop('payload')
            messages.append(Message(channel=None, auto_decode=True, **message))
        return messages
