import json

from amqpstorm.compatibility import quote
from amqpstorm.management.base import ManagementHandler

API_USER = 'users/%s'
API_USERS = 'users'
API_USER_VIRTUAL_HOST_PERMISSIONS = 'permissions/%s/%s'
API_USER_PERMISSIONS = 'users/%s/permissions'


class User(ManagementHandler):
    def get(self, username):
        """Get User details.

        :param str username: Username

        :rtype: dict
        """
        return self.config.http_client.get(API_USER % username)

    def list(self):
        """List all Users.

        :rtype: list
        """
        return self.config.http_client.get(API_USERS)

    def create(self, username, password, tags=''):
        """Create User.

        :param str username: Username
        :param str password: Password
        :param str tags: Comma-separate list of tags (e.g. monitoring)

        :rtype: None
        """
        user_payload = json.dumps({
            'password': password,
            'tags': tags
        })
        return self.config.http_client.put(API_USER % username,
                                           payload=user_payload)

    def delete(self, username):
        """Delete User.

        :param str username: Username

        :rtype: dict
        """
        return self.config.http_client.delete(API_USER % username)

    def get_permission(self, username, virtual_host):
        """Get a User permissions for a specific virtual host.

        :param str username: Username
        :param str virtual_host: Virtual host

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.config.http_client.get(API_USER_VIRTUAL_HOST_PERMISSIONS %
                                           (
                                               virtual_host,
                                               username
                                           ))

    def get_permissions(self, username):
        """Get all Users permissions.

        :param str username: Username

        :rtype: dict
        """
        return self.config.http_client.get(API_USER_PERMISSIONS %
                                           (
                                               username
                                           ))

    def set_permission(self, username, virtual_host, configure_regex='.*',
                       write_regex='.*', read_regex='.*'):
        """Set a Users permissions.

        :param str username: Username
        :param str virtual_host: Virtual host
        :param str configure_regex: Permission pattern for configuration 
                                    operations for this user.
        :param str write_regex: Permission pattern for write operations 
                                for this user.
        :param str read_regex: Permission pattern for read operations 
                               for this user.

        :rtype: dict
        """
        permission_payload = json.dumps({
            "configure": configure_regex,
            "read": read_regex,
            "write": write_regex
        })
        return self.config.http_client.put(API_USER_VIRTUAL_HOST_PERMISSIONS %
                                           (
                                               virtual_host,
                                               username
                                           ), payload=permission_payload)

    def delete_permission(self, username, virtual_host):
        """Delete a Users permissions.

        :param str username: Username
        :param str virtual_host: Virtual host

        :rtype: dict
        """
        return self.config.http_client.delete(
            API_USER_VIRTUAL_HOST_PERMISSIONS %
            (
                virtual_host,
                username
            ))
