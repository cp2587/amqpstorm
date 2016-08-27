from amqpstorm.compatibility import quote
from amqpstorm.management.base import ManagementHandler

API_VIRTUAL_HOST = 'vhosts/%s'
API_VIRTUAL_HOSTS = 'vhosts'
API_VIRTUAL_HOSTS_PERMISSION = 'vhosts/%s/permissions'


class VirtualHost(ManagementHandler):
    def get(self, virtual_host):
        """Get Virtual Host details.

        :param str virtual_host: Virtual host name

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.config.http_client.get(API_VIRTUAL_HOST % virtual_host)

    def list(self):
        """List all Virtual Hosts.

        :rtype: list
        """
        return self.config.http_client.get(API_VIRTUAL_HOSTS)

    def create(self, virtual_host):
        """Create a Virtual Host.

        :param str virtual_host: Virtual host name

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.config.http_client.put(API_VIRTUAL_HOST % virtual_host)

    def delete(self, virtual_host):
        """Delete a Virtual Host.

        :param str virtual_host: Virtual host name

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.config.http_client.delete(API_VIRTUAL_HOST % virtual_host)

    def get_permissions(self, virtual_host):
        """Get all Virtual hosts permissions.

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.config.http_client.get(API_VIRTUAL_HOSTS_PERMISSION %
                                           (
                                               virtual_host
                                           ))
