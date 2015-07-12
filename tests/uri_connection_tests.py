__author__ = 'eandersson'

import sys
import ssl
import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm import UriConnection


logging.basicConfig(level=logging.DEBUG)


@unittest.skipIf(sys.version_info < (2, 7),
                 'UriConnection not supported in Python 2.6')
class UriConnectionTests(unittest.TestCase):
    def test_default_uri(self):
        connection = \
            UriConnection('amqp://guest:guest@localhost:5672/%2F?lazy')
        self.assertEqual(connection.parameters['hostname'], 'localhost')
        self.assertEqual(connection.parameters['username'], 'guest')
        self.assertEqual(connection.parameters['password'], 'guest')
        self.assertEqual(connection.parameters['virtual_host'], '/')
        self.assertEqual(connection.parameters['port'], 5672)
        self.assertEqual(connection.parameters['heartbeat'], 60)
        self.assertEqual(connection.parameters['timeout'], 30)
        self.assertFalse(connection.parameters['ssl'])

    def test_uri_set_hostname(self):
        connection = \
            UriConnection('amqp://guest:guest@my-server:5672/%2F?lazy&'
                          'heartbeat=1337')
        self.assertEqual(connection.parameters['hostname'], 'my-server')

    def test_uri_set_username(self):
        connection = \
            UriConnection('amqp://username:guest@localhost:5672/%2F?lazy&'
                          'heartbeat=1337')
        self.assertEqual(connection.parameters['username'], 'username')

    def test_uri_set_password(self):
        connection = \
            UriConnection('amqp://guest:password@localhost:5672/%2F?lazy&'
                          'heartbeat=1337')
        self.assertEqual(connection.parameters['password'], 'password')

    def test_uri_set_port(self):
        connection = \
            UriConnection('amqp://guest:guest@localhost:1337/%2F?lazy')
        self.assertEqual(connection.parameters['port'], 1337)

    def test_uri_set_heartbeat(self):
        connection = \
            UriConnection('amqp://guest:guest@localhost:5672/%2F?lazy&'
                          'heartbeat=1337')
        self.assertEqual(connection.parameters['heartbeat'], 1337)

    def test_uri_set_timeout(self):
        connection = \
            UriConnection('amqp://guest:guest@localhost:5672/%2F?lazy&'
                          'timeout=1337')
        self.assertEqual(connection.parameters['timeout'], 1337)

    def test_uri_set_virtual_host(self):
        connection = \
            UriConnection('amqp://guest:guest@localhost:5672/travis?lazy')
        self.assertEqual(connection.parameters['virtual_host'], 'travis')

    def test_uri_set_ssl(self):
        connection = UriConnection('amqps://guest:guest@localhost:5671/%2F?'
                                   'lazy&'
                                   'ssl_version=protocol_sslv3&'
                                   'cert_reqs=cert_required&'
                                   'keyfile=file.key&'
                                   'certfile=file.crt&'
                                   'ca_certs=test')
        self.assertTrue(connection.parameters['ssl'])
        self.assertEqual(connection.parameters['ssl_options']['ssl_version'],
                         ssl.PROTOCOL_SSLv3)
        self.assertEqual(connection.parameters['ssl_options']['cert_reqs'],
                         ssl.CERT_REQUIRED)
        self.assertEqual(connection.parameters['ssl_options']['keyfile'],
                         'file.key')
        self.assertEqual(connection.parameters['ssl_options']['certfile'],
                         'file.crt')
        self.assertEqual(connection.parameters['ssl_options']['ca_certs'],
                         'test')