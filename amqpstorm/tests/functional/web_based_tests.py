import logging
import uuid
import time

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm import Connection
from amqpstorm.tests.functional import HOST
from amqpstorm.tests.functional import HTTP_URL
from amqpstorm.tests.functional import USERNAME
from amqpstorm.tests.functional import PASSWORD
from amqpstorm.exception import AMQPConnectionError
from amqpstorm.management import ManagementApi

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


class WebFunctionalTests(unittest.TestCase):
    connection = None
    channel = None

    def test_functional_client_properties(self):
        self.connection = Connection(HOST, USERNAME, PASSWORD)
        self.channel = self.connection.channel()

        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        client_properties = api.connection.list()[0]['client_properties']

        result = self.connection._channel0._client_properties()

        self.assertIsInstance(result, dict)
        self.assertEqual(result['information'],
                         client_properties['information'])
        self.assertEqual(result['product'], client_properties['product'])
        self.assertEqual(result['platform'], client_properties['platform'])

        self.connection.close()

    def test_functional_consume_web_message(self):
        message = str(uuid.uuid4())
        queue = 'test_functional_consume_web_message'

        self.connection = Connection(HOST, USERNAME, PASSWORD)
        self.channel = self.connection.channel()

        try:
            self.channel.queue.declare(queue)

            api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
            api.basic.publish(body=message, routing_key=queue)

            time.sleep(0.1)

            result = self.channel.basic.get(queue)

            self.assertEqual(result.body, message)
        finally:
            self.channel.queue.delete(queue)

    def test_functional_connection_forcefully_closed(self):
        self.connection = Connection(HOST, USERNAME, PASSWORD, timeout=1)
        self.channel = self.connection.channel()

        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        for connection in api.connection.list():
            api.connection.close(connection['name'])

        time.sleep(0.1)

        self.assertRaises(AMQPConnectionError, self.channel.basic.publish,
                          'body', 'routing_key')

        self.assertRaisesRegexp(AMQPConnectionError,
                                'Connection was closed by remote server: '
                                'CONNECTION_FORCED - '
                                'Closed via management api',
                                self.channel.check_for_errors)

        self.assertRaisesRegexp(AMQPConnectionError,
                                'Connection was closed by remote server: '
                                'CONNECTION_FORCED - '
                                'Closed via management api',
                                self.connection.check_for_errors)

    def test_functional_alternative_virtual_host(self):
        vhost_name = 'travis_ci'
        queue = 'test_functional_alternative_virtual_host'

        api = ManagementApi(HTTP_URL, USERNAME, PASSWORD)
        api.virtual_host.create(vhost_name)

        api.user.set_permission('guest', vhost_name)

        self.connection = Connection(HOST, USERNAME, PASSWORD,
                                     virtual_host=vhost_name)
        self.channel = self.connection.channel()
        self.channel.queue.declare(queue)
        self.channel.queue.delete(queue)
        api.user.delete_permission('guest', vhost_name)
        api.virtual_host.delete(vhost_name)
